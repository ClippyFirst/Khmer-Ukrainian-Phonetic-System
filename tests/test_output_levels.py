from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_shared_strictness_labels_preserve_existing_semantics():
    html = (ROOT / "index.html").read_text(encoding="utf-8")
    main = (ROOT / "src" / "main.js").read_text(encoding="utf-8")
    engine = (ROOT / "src" / "khmer-engine-core.js").read_text(encoding="utf-8")

    assert '<option value="strict">Strict ·' in html
    assert '<option value="balanced" selected>Soft ·' in html
    assert '<option value="exploratory">Super-soft ·' in html

    assert 'strict: "Strict: лише детерміновані правила' in main
    assert 'balanced: "Soft: додає точні словникові фонемні записи Google, повні CV/CVC-кандидати' in main
    assert 'exploratory: "Super-soft: додатково використовує статичні детерміновані OOV-кандидати' in main
    assert 'outputLevel !== "strict"' in engine


def test_strictness_labels_are_not_confidence_or_accuracy_claims():
    policy = (ROOT / "docs" / "BETA-RELEASE-POLICY.md").read_text(encoding="utf-8")
    assert "These are disclosure/acceptance levels" in policy
    assert "not complete syllables, IPA or confirmed Ukrainian pronunciation" in policy
