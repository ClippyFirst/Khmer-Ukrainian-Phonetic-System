import json

from khmer_ua.cli import main


def test_analyze_cli_exposes_typed_ipa_result(monkeypatch, capsys):
    monkeypatch.setattr("sys.argv", ["khmer-ua", "analyze", "ខ្មែរ"])

    main()

    result = json.loads(capsys.readouterr().out)
    assert result["phonetic_result"]["units"][0]["typed_ipa"]["status"] == "UNCERTAIN"
    assert result["phonetic_result"]["units"][0]["ukrainian"] == "к'мае"


def test_ipa_cli_shows_partial_onset_and_unknown_remainder(monkeypatch, capsys):
    monkeypatch.setattr("sys.argv", ["khmer-ua", "ipa", "ក្ក"])

    main()

    assert capsys.readouterr().out.strip() == "k???"


def test_transliterate_cli_shows_ipa_derived_provisional_result(monkeypatch, capsys):
    monkeypatch.setattr("sys.argv", ["khmer-ua", "transliterate", "ក្ក"])

    main()

    assert capsys.readouterr().out.strip() == "к???"


def test_ipa_cli_uses_three_question_marks_when_no_hint_exists(monkeypatch, capsys):
    monkeypatch.setattr("sys.argv", ["khmer-ua", "ipa", "្"])

    main()

    assert capsys.readouterr().out.strip() == "???"
