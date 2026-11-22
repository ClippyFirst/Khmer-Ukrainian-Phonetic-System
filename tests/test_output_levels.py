from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_shared_strictness_labels_preserve_existing_semantics():
    html = (ROOT / "index.html").read_text(encoding="utf-8")
    engine = (ROOT / "src" / "main.js").read_text(encoding="utf-8")

    assert '<option value="strict">Strict ·' in html
    assert '<option value="balanced" selected>Soft ·' in html
    assert '<option value="exploratory">Super-soft ·' in html

    assert 'strict: "Обережний рівень:' in engine
    assert 'balanced: "Збалансований рівень:' in engine
    assert 'exploratory: "Дослідницький рівень:' in engine
    assert 'item.fallback_status === "PROVISIONAL"' in engine
    assert 'outputLevelMode !== "strict"' not in engine


def test_strictness_labels_are_not_confidence_or_accuracy_claims():
    policy = (ROOT / "docs" / "BETA-RELEASE-POLICY.md").read_text(encoding="utf-8")
    assert "These are disclosure/acceptance levels" in policy
    assert "not complete syllables, IPA or confirmed Ukrainian pronunciation" in policy
