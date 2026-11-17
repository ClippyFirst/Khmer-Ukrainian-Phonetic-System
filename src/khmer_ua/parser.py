import unicodedata
from .normalize import normalize_khmer
from .data import CONSONANTS, SIGNS, SHIFTER_ELIGIBILITY
from .model import KhmerGrapheme, KhmerSyllable, AnalysisResult
from .phonology import resolve_effective_register
from .orthographic_structure import scan_orthographic_components

COENG="្"
MUUSIKATOAN="៉"
TRIISAP="៊"
ZWNJ="\u200C"
ZWSP="\u200B"
INDEPENDENT_VOWELS={x["char"] for x in SIGNS if x.get("kind")=="independent_vowel"}

def _lookup(ch):
    return next((x for x in CONSONANTS if x["char"]==ch), None)


def khmer_subscript_sequence_spans(text: str) -> tuple[tuple[int, int], ...]:
    """Return exact-source spans for Unicode-structured COENG + following units.

    The returned half-open code-point intervals protect only the encoded
    subscript pair. They are not complete orthographic-syllable or word spans.
    A pair is recognized only when the following code point is a modeled Khmer
    consonant or independent vowel; malformed sequences are left unprotected.
    """
    chars = list(text)
    return tuple(
        (index, index + 2)
        for index, char in enumerate(chars[:-1])
        if char == COENG and (_lookup(chars[index + 1]) or chars[index + 1] in INDEPENDENT_VOWELS)
    )

def _starts_new_orthographic_syllable(chars, i):
    """Conservatively split explicit Khmer syllable boundaries."""
    if not _lookup(chars[i]):
        return False
    if i == 0:
        return False
    if chars[i-1] == COENG:
        return False
    # Unicode 18 Chapter 16 documents subscript independent-vowel sequences
    # with a following coda consonant (for example, ផ្ឯម) as one orthographic
    # unit. Do not split immediately after the subscript independent vowel.
    if i >= 2 and chars[i-2] == COENG and chars[i-1] in INDEPENDENT_VOWELS:
        return False
    if i + 1 < len(chars) and chars[i+1] == COENG:
        return False
    previous_kind = next((x["kind"] for x in SIGNS if x["char"] == chars[i-1]), None)
    if previous_kind in {"dependent_vowel", "composite_vowel", "vowel_modifier", "sign"}:
        j = i + 1
        if j >= len(chars) or chars[j].isspace() or unicodedata.category(chars[j]).startswith("P"):
            return False
    return True

def _script_bucket(char: str) -> str | None:
    """Classify a source character for safe mixed-script token boundaries.

    Khmer letters/marks stay in the Khmer run. Combining marks inherit the
    preceding run. Numbers are handled as separate non-phonetic literals.
    Other letters are kept together as foreign-script runs.
    """
    codepoint = ord(char)
    category = unicodedata.category(char)
    if char == ZWNJ:
        return None
    if category.startswith("N"):
        return "number"
    if 0x1780 <= codepoint <= 0x17FF or 0x19E0 <= codepoint <= 0x19FF:
        return "khmer"
    if category.startswith("M"):
        return None
    if category.startswith("L"):
        return "foreign"
    return "other"


def segment_syllables(text: str) -> list[str]:
    """Preserve separators and split Khmer, foreign-script and numeric runs.

    Khmer orthographic segmentation remains conservative and is not lexical
    word segmentation. Foreign-script text and numeric literals are isolated
    so they cannot poison an adjacent Khmer orthographic unit.
    """
    units: list[str] = []
    current: list[str] = []
    current_bucket: str | None = None
    chars = list(text)
    i = 0

    def flush() -> None:
        nonlocal current_bucket
        if current:
            units.append("".join(current))
            current.clear()
        current_bucket = None

    while i < len(chars):
        ch = chars[i]
        if ch == ZWSP or ch.isspace() or unicodedata.category(ch).startswith("P"):
            flush()
            units.append(ch)
            i += 1
            continue

        bucket = _script_bucket(ch)
        if bucket == "number":
            flush()
            numeric: list[str] = []
            while i < len(chars) and unicodedata.category(chars[i]).startswith("N"):
                numeric.append(chars[i])
                i += 1
            units.append("".join(numeric))
            continue

        effective_bucket = bucket or current_bucket or "other"
        if current and current_bucket is not None and effective_bucket != current_bucket:
            flush()
        if not current:
            current_bucket = effective_bucket

        if current and effective_bucket == "khmer" and _starts_new_orthographic_syllable(chars, i):
            flush()
            current_bucket = "khmer"
        current.append(ch)
        i += 1

    flush()
    return units

def decompose_khmer_syllable(raw: str) -> KhmerSyllable:
    n=normalize_khmer(raw)
    s=KhmerSyllable(raw_text=raw, normalized_text=n)
    chars=list(n); i=0
    while i<len(chars):
        ch=chars[i]
        if ch==ZWNJ:
            s.graphemes.append(KhmerGrapheme(ch,"format_control",(f"U+{ord(ch):04X}",)))
            i+=1
            continue
        if ch==COENG:
            if i+1>=len(chars) or not (_lookup(chars[i+1]) or chars[i+1] in INDEPENDENT_VOWELS):
                # Preserve malformed coeng and every following code point in
                # the trace. Structural failure must never erase source text.
                for remaining in chars[i:]:
                    s.graphemes.append(
                        KhmerGrapheme(remaining,"invalid_sequence_component",(f"U+{ord(remaining):04X}",))
                    )
                s.status="INVALID_OR_UNSUPPORTED"
                s.confidence=0.0
                s.sources=["unicode17-ch16"]
                return s
            sub=chars[i+1]
            if _lookup(sub):
                s.subscripts.append(sub)
                kind = "subscript"
            else:
                s.subscript_independent_vowels.append(sub)
                kind = "subscript_independent_vowel"
            s.graphemes.append(KhmerGrapheme(COENG+sub,kind,(f"U+{ord(COENG):04X}",f"U+{ord(sub):04X}")))
            i+=2
            continue
        c=_lookup(ch)
        if c:
            if s.base_consonant is None:
                s.base_consonant=ch
            s.graphemes.append(KhmerGrapheme(ch,"consonant",(f"U+{ord(ch):04X}",)))
        elif ch in INDEPENDENT_VOWELS:
            s.independent_vowel=ch
            s.graphemes.append(KhmerGrapheme(ch,"independent_vowel",(f"U+{ord(ch):04X}",)))
        else:
            kind=next((x["kind"] for x in SIGNS if x["char"]==ch),"sign_or_unknown")
            if kind in {"sign_or_unknown", "unmodeled_letter"}:
                # Do not let an unrecognized or explicitly unmodelled letter
                # inherit ESTABLISHED_STRUCTURE from a valid Khmer base. Keep
                # the entire remaining source tail visible in the trace.
                for offset, remaining in enumerate(chars[i:]):
                    remaining_kind = kind if offset == 0 else "unparsed_after_unsupported"
                    s.graphemes.append(
                        KhmerGrapheme(remaining,remaining_kind,(f"U+{ord(remaining):04X}",))
                    )
                s.sources=["unicode17-ch16"]
                s.status="INVALID_OR_UNSUPPORTED"
                s.confidence=0.0
                return s
            if kind in {"dependent_vowel","composite_vowel","vowel_modifier"}:
                s.vowel_signs.append(ch)
            s.graphemes.append(KhmerGrapheme(ch,kind,(f"U+{ord(ch):04X}",)))
        i+=1
    if s.base_consonant:
        c=_lookup(s.base_consonant)
        s.register, shifter_rule=resolve_effective_register(c, chars)
        s.inherent_vowel=("first-series" if s.register=="first" else "second-series" if s.register=="second" else None)
        s.phonology["onset_ipa"]=("p" if s.base_consonant=="ប" and shifter_rule=="BA_TO_PA_EXCEPTION" else c.get("onset_ipa"))
        if shifter_rule:
            s.phonology["register_shifter"]=shifter_rule
        s.sources=["unicode17-ch16"]
        if s.subscript_independent_vowels:
            s.sources.append("unicode18-ch16")
        s.status="ESTABLISHED_STRUCTURE" if shifter_rule not in {"MULTIPLE_REGISTER_SHIFTERS", "MISPLACED_REGISTER_SHIFTER", "NON_STANDARD_SHIFTER_USE"} else "EVIDENCE_LIMITED"
        s.confidence=0.9 if s.status=="ESTABLISHED_STRUCTURE" else 0.6
    elif s.independent_vowel:
        s.sources=["unicode17-ch16"]
        if s.subscript_independent_vowels:
            s.sources.append("unicode18-ch16")
        s.status="ESTABLISHED_STRUCTURE"
        s.confidence=0.9
    else:
        s.status="INVALID_OR_UNSUPPORTED"
        s.confidence=0.0
    return s

def analyze(text: str) -> AnalysisResult:
    n=normalize_khmer(text)
    units=segment_syllables(n)
    linguistic_units=[x for x in units if x.strip() and x != ZWSP and not unicodedata.category(x[0]).startswith("P")]
    syllables=[decompose_khmer_syllable(x) for x in linguistic_units]
    sg=[]
    for s in syllables:
        component_scan = scan_orthographic_components(s.normalized_text).to_dict()
        sg.append({
            "raw_text":s.raw_text,"normalized_text":s.normalized_text,
            "graphemes":[{"text":g.text,"kind":g.kind,"codepoints":g.codepoints} for g in s.graphemes],
            "base_consonant":s.base_consonant,"register":s.register,
            "subscripts":s.subscripts,"subscript_independent_vowels":s.subscript_independent_vowels,"vowel_signs":s.vowel_signs,
            "independent_vowel":s.independent_vowel,"inherent_vowel":s.inherent_vowel,
            "phonology":s.phonology,
            "status":s.status,"confidence":s.confidence,"sources":s.sources,
            "orthographic_structure_status":component_scan["status"],
            "orthographic_components":component_scan["components"],
            "orthographic_structure_notes":component_scan["notes"]})
    invalid_count=sum(1 for s in sg if s["status"]=="INVALID_OR_UNSUPPORTED")
    if not syllables:
        overall_status = "INVALID_OR_UNSUPPORTED"
    elif invalid_count == len(sg):
        overall_status = "INVALID_OR_UNSUPPORTED"
    elif invalid_count or any(s["status"] == "EVIDENCE_LIMITED" for s in sg):
        overall_status = "EVIDENCE_LIMITED"
    else:
        overall_status = "ESTABLISHED_STRUCTURE"

    analysis_sources = ["unicode17-ch16"]
    if any("unicode18-ch16" in syllable.sources for syllable in syllables):
        analysis_sources.append("unicode18-ch16")
    return AnalysisResult(text,n,[],sg,{"syllables":sg},{"status":"phoneticization_not_yet_established"},
                          None,[],[],None,[],[],analysis_sources,
                          min((s.confidence for s in syllables),default=0.0),
                          overall_status)
