"""Small CPU-only encoder/decoder used only for offline phonemic teacher training."""
from __future__ import annotations

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
        self.decoder = nn.GRU(embedding_size, hidden_size, batch_first=True)
        self.output = nn.Linear(hidden_size, target_vocab_size)

    def encode(self, source: torch.Tensor, source_lengths: torch.Tensor) -> torch.Tensor:
        embedded = self.source_embedding(source)
        packed = pack_padded_sequence(
            embedded, source_lengths.cpu(), batch_first=True, enforce_sorted=False
        )
        _outputs, hidden = self.encoder(packed)
        combined = torch.cat((hidden[-2], hidden[-1]), dim=-1)
        return torch.tanh(self.initial_state(combined)).unsqueeze(0)

    def forward(
        self,
        source: torch.Tensor,
        source_lengths: torch.Tensor,
        target_input: torch.Tensor,
    ) -> torch.Tensor:
        hidden = self.encode(source, source_lengths)
        embedded = self.target_embedding(target_input)
        decoded, _ = self.decoder(embedded, hidden)
        return self.output(decoded)

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
        hidden = self.encode(source, source_lengths)
        batch_size = source.shape[0]
        previous = torch.full(
            (batch_size, 1), bos_id, dtype=torch.long, device=source.device
        )
        finished = torch.zeros(batch_size, dtype=torch.bool, device=source.device)
        outputs: list[list[int]] = [[] for _ in range(batch_size)]
        for _ in range(max_length):
            embedded = self.target_embedding(previous)
            decoded, hidden = self.decoder(embedded, hidden)
            next_token = self.output(decoded[:, -1]).argmax(dim=-1)
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
