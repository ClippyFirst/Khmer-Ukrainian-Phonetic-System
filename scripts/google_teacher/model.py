"""Attention-based CPU encoder/decoder for offline Khmer phonemic teacher training."""
from __future__ import annotations

import math

import torch
from torch import nn
from torch.nn.utils.rnn import pack_padded_sequence, pad_packed_sequence


class KhmerPhonemicSeq2Seq(nn.Module):
    def __init__(
        self,
        source_vocab_size: int,
        target_vocab_size: int,
        *,
        embedding_size: int = 96,
        hidden_size: int = 128,
        padding_index: int = 0,
    ) -> None:
        super().__init__()
        self.hidden_size = hidden_size
        self.source_embedding = nn.Embedding(
            source_vocab_size, embedding_size, padding_idx=padding_index
        )
        self.target_embedding = nn.Embedding(
            target_vocab_size, embedding_size, padding_idx=padding_index
        )
        self.encoder = nn.GRU(
            embedding_size, hidden_size, batch_first=True, bidirectional=True
        )
        self.initial_state = nn.Linear(hidden_size * 2, hidden_size)
        self.attention_query = nn.Linear(hidden_size, hidden_size * 2, bias=False)
        self.decoder = nn.GRU(
            embedding_size + hidden_size * 2, hidden_size, batch_first=True
        )
        self.output = nn.Linear(hidden_size * 3, target_vocab_size)

    def encode(
        self, source: torch.Tensor, source_lengths: torch.Tensor
    ) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
        embedded = self.source_embedding(source)
        packed = pack_padded_sequence(
            embedded, source_lengths.cpu(), batch_first=True, enforce_sorted=False
        )
        packed_outputs, hidden = self.encoder(packed)
        encoder_outputs, _ = pad_packed_sequence(
            packed_outputs, batch_first=True, total_length=source.shape[1]
        )
        combined = torch.cat((hidden[-2], hidden[-1]), dim=-1)
        initial = torch.tanh(self.initial_state(combined)).unsqueeze(0)
        positions = torch.arange(source.shape[1], device=source.device).unsqueeze(0)
        mask = positions < source_lengths.to(source.device).unsqueeze(1)
        return encoder_outputs, mask, initial

    def _decode_step(
        self,
        previous: torch.Tensor,
        encoder_outputs: torch.Tensor,
        source_mask: torch.Tensor,
        hidden: torch.Tensor,
    ) -> tuple[torch.Tensor, torch.Tensor]:
        query = self.attention_query(hidden[-1])
        scores = torch.bmm(encoder_outputs, query.unsqueeze(-1)).squeeze(-1)
        scores = scores / math.sqrt(encoder_outputs.shape[-1])
        scores = scores.masked_fill(~source_mask, torch.finfo(scores.dtype).min)
        weights = torch.softmax(scores, dim=-1)
        context = torch.bmm(weights.unsqueeze(1), encoder_outputs)
        embedded = self.target_embedding(previous)
        decoder_input = torch.cat((embedded, context), dim=-1)
        decoded, next_hidden = self.decoder(decoder_input, hidden)
        logits = self.output(torch.cat((decoded, context), dim=-1))
        return logits, next_hidden

    def forward(
        self,
        source: torch.Tensor,
        source_lengths: torch.Tensor,
        target_input: torch.Tensor,
    ) -> torch.Tensor:
        encoder_outputs, source_mask, hidden = self.encode(source, source_lengths)
        outputs = []
        for position in range(target_input.shape[1]):
            logits, hidden = self._decode_step(
                target_input[:, position:position + 1],
                encoder_outputs,
                source_mask,
                hidden,
            )
            outputs.append(logits)
        return torch.cat(outputs, dim=1)

    @torch.inference_mode()
    def greedy_decode(
        self,
        source: torch.Tensor,
        source_lengths: torch.Tensor,
        *,
        bos_id: int,
        eos_id: int,
        max_length: int = 64,
    ) -> list[list[int]]:
        encoder_outputs, source_mask, hidden = self.encode(source, source_lengths)
        batch_size = source.shape[0]
        previous = torch.full(
            (batch_size, 1), bos_id, dtype=torch.long, device=source.device
        )
        finished = torch.zeros(batch_size, dtype=torch.bool, device=source.device)
        outputs: list[list[int]] = [[] for _ in range(batch_size)]
        for _ in range(max_length):
            logits, hidden = self._decode_step(
                previous, encoder_outputs, source_mask, hidden
            )
            next_token = logits[:, -1].argmax(dim=-1)
            for index, token in enumerate(next_token.tolist()):
                if not finished[index]:
                    if token == eos_id:
                        finished[index] = True
                    else:
                        outputs[index].append(token)
            previous = next_token.unsqueeze(1)
            if bool(finished.all()):
                break
        return outputs
