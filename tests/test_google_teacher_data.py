from khmer_ua.google_teacher_data import (
    build_google_teacher_dataset,
    load_google_teacher_dataset,
    split_for_word,
    tokenize_source,
    tokenize_target,
    validate_word_disjoint_splits,
)


def test_teacher_tokenizers_keep_source_codepoints_and_phone_tokens_atomic():
    assert tokenize_source("ក") == ("ក",)
    assert tokenize_target("ph ie . s aa") == ("ph", "ie", ".", "s", "aa")


def test_teacher_split_is_deterministic_and_groups_variants_by_spelling():
    assert split_for_word("ការី", 17) == split_for_word("ការី", 17)
    assert split_for_word("ក", 17) in {"train", "dev", "test"}
    dataset = load_google_teacher_dataset()
    validate_word_disjoint_splits(dataset)
    assert all(
        len({dataset.split_by_word[row.word] for row in dataset.examples if row.word == word}) == 1
        for word in dataset.split_by_word
    )


def test_teacher_dataset_uses_only_single_syllable_aligned_pairs():
    dataset = load_google_teacher_dataset()
    assert dataset.examples
    assert any(row.word == "ក" for row in dataset.examples)
    assert all("." not in row.target_tokens for row in dataset.examples)
    assert all(row.source_tokens == tokenize_source(row.word) for row in dataset.examples)
    assert set(dataset.split_by_word.values()) == {"train", "dev", "test"}
    manifest = dataset.manifest()
    assert manifest["label_semantics"].startswith("Google source phonemic labels")
    assert manifest["alignment_policy"].startswith("one unambiguous Unicode orthographic syllable")
    assert manifest["source_revision"] == "a90601024f07ab7e96c911243324e0adeb16da96"


def test_teacher_dataset_rebuild_is_stable():
    first = build_google_teacher_dataset(seed=1234)
    second = build_google_teacher_dataset(seed=1234)
    assert first.examples == second.examples
    assert first.split_by_word == second.split_by_word
    assert first.manifest() == second.manifest()
