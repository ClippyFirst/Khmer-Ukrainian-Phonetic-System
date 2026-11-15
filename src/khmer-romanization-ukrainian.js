// Orthographic rendering of BGN/PCGN Khmer romanization into Ukrainian.
// This path is independent of IPA. Ukrainian targets remain project proposals;
// unknown Latin fragments are bracketed rather than guessed.
const MAP = Object.freeze({
  // Multi-character and contextual BGN/PCGN vowel forms (longest match wins).
  eăng:"еанг", ăng:"анг", "ŏâm":"оам", aôh:"аог", "ŏăh":"оаг",
  eăh:"еаг", ăh:"аг", ŏh:"ог", ŭh:"уг", éh:"ег",
  "rœ̆":"ри", "lœ̆":"ли", "rœ":"ри", "lœ":"ли",
  "œ̆":"и", "œă":"иа", œ:"и",
  "uŏ":"уо", aô:"ао", oŭ:"оу", "éa":"еа", eă:"еа", oă:"оа", "iĕ":"іє",
  aeu:"аеу", eu:"еу",
  chh:"ч'", kh:"к'", th:"т'", ph:"п'", nh:"нь", ng:"нг", ch:"ч",
  // Vowel + coda combinations and ASCII forms retained by the upstream package.
  om:"ом", ŭm:"ум", âm:"ам", um:"ум", ăm:"ам", ai:"ай", ey:"ей", ei:"ей",
  au:"ау", "ŏu":"оу", ou:"оу", ae:"ае", oea:"иа", roe:"ри", loe:"ли", oe:"и",
  uo:"уо", oam:"оам", aoh:"аог", oah:"оаг", eah:"еаг", ah:"аг", oh:"ог",
  uh:"уг", eh:"ег", eang:"еанг", ang:"анг", ao:"ао",
  // Single-character PCGN vowel values.
  â:"а", ô:"о", á:"а", ó:"о", ă:"а", ĕ:"е", ĭ:"і", ŏ:"о", ŭ:"у",
  é:"е", ê:"е",
  a:"а", e:"е", i:"і", o:"о", u:"у",
  // Consonants.
  b:"б", d:"д", k:"к", l:"л", m:"м", n:"н", p:"п", r:"р", s:"с",
  t:"т", v:"в", y:"й", h:"г",
  "’":"ʼ", "'":"ʼ",
  c:null, f:null, g:null, j:null, q:null, w:null, x:null, z:null,
});
const KEYS=Object.keys(MAP).sort((a,b)=>b.length-a.length);
const isKhmer=char=>{
  const cp=char.codePointAt(0);
  return (cp>=0x1780&&cp<=0x17ff)||(cp>=0x19e0&&cp<=0x19ff);
};

export function renderLatinWord(value){
  const input=String(value??"").normalize("NFC");
  let output="",unsupported=0,mapped=0;
  for(let i=0;i<input.length;){
    const rest=input.slice(i);
    const key=KEYS.find(candidate=>rest.toLowerCase().startsWith(candidate));
    if(!key){
      const char=String.fromCodePoint(input.codePointAt(i));
      const codePoint=char.codePointAt(0);
      if(codePoint>=0x17e0&&codePoint<=0x17e9){output+=String(codePoint-0x17e0);mapped+=1;}
      else if(/\p{Script=Latin}/u.test(char)){output+="⟦"+char+"⟧";unsupported+=1;}
      else output+=char;
      i+=char.length;
      continue;
    }
    const source=input.slice(i,i+key.length),target=MAP[key];
    if(target===null){output+="⟦"+source+"⟧";unsupported+=1;}
    else{
      const hasCasedLetter=/\p{L}/u.test(source);
      const allUpper=hasCasedLetter&&source===source.toLocaleUpperCase("en");
      const startsUpper=/^\p{Lu}/u.test(source);
      const cased=allUpper
        ? target.toLocaleUpperCase("uk")
        : startsUpper
          ? target[0].toLocaleUpperCase("uk")+target.slice(1)
          : target;
      output+=cased;
      mapped+=1;
    }
    i+=key.length;
  }
  return {text:output,mapped,unsupported};
}

export function renderRomanizedText(source){
  const input=String(source??"").normalize("NFC");
  const rendered=renderLatinWord(input);
  const hasLatin=/\p{Script=Latin}/u.test(input);
  return {
    ...rendered,
    status:!hasLatin?"PASSTHROUGH":rendered.unsupported?"PARTIAL":"PROVISIONAL",
    profile:"BGN/PCGN 1972 romanization input; Ukrainian target values are project proposals",
  };
}

export function renderKhmerRomanizationText(source,romanizer){
  const chars=[...String(source??"").normalize("NFC")];
  let output="",mapped=0,unsupported=0,hasKhmer=false;
  for(let i=0;i<chars.length;){
    if(!isKhmer(chars[i])){output+=chars[i];i+=1;continue;}
    hasKhmer=true;
    let run="";
    while(i<chars.length&&isKhmer(chars[i])){run+=chars[i];i+=1;}
    const latin=romanizer(run);
    const rendered=renderLatinWord(latin);
    output+=rendered.text;
    mapped+=rendered.mapped;
    unsupported+=rendered.unsupported;
  }
  return {
    text:output,
    status:!hasKhmer?"PASSTHROUGH":unsupported?"PARTIAL":"PROVISIONAL",
    mapped,unsupported,
    profile:"BGN/PCGN-derived ASCII (diacritics omitted upstream)",
  };
}
