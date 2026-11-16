from khmer_ua import map_sequence, render_ipa_profile

def test_public_api_exports_research_functions():
    assert map_sequence(["kʰ", "a"]) == "к\u0027а"
    assert render_ipa_profile("krɑː", "khmer-pph-careful-citation-v1") == "krɑː"


def test_public_api_exports_orthographic_component_scanner():
    from khmer_ua import scan_orthographic_components

    scan = scan_orthographic_components("ខ្ញុំ")
    assert scan.status == "ESTABLISHED_STRUCTURE"
    assert scan.components[1].role == "SUBSCRIPT"
