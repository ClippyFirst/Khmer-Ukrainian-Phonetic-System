# Детермінований кмерський рушій

Публічний браузерний рушій детермінований під час виконання: він не запускає нейромережу, не завантажує ваги, не викликає ONNX Runtime і не надсилає текст на сервер. Нейромережа використовується лише офлайн під час складання: її фонемні прогнози компілюються в статичну таблицю кандидатів, яку сайт читає як звичайні дані. Python API залишається окремим правиловим рушієм.

## Конвеєр

1. NFC-нормалізація та сегментація кмерського письма.
2. Структурний розбір приголосних, підрядкових знаків, голосних і регістрових маркерів.
3. Для лексичних винятків — точний пошук у версійованих джерельних прикладах і Google-фонемному лексиконі.
4. Google phone tokens проходять через окремий evidence-aware адаптер GOOGLE_PHONEMIC → typed IPA; вони не є готовою IPA.
5. Для вузького класу підтриманих структур — застосування явного правила серії та притаманного голосного.
6. У Super-soft — точний пошук у статичній таблиці OOV-кандидатів, отриманій офлайновою дистиляцією нейромережевого вчителя.
7. Єдиний IPA → українська адаптер формує практичний запис.

## Детермінованість і межі

Однаковий нормалізований ввід, версія правил і набір даних дають однаковий результат. Це властивість обчислення, а не автоматичний доказ фонетичної істинності. Статус `PROPOSED` залишається запропонованим; непідтримані підрядкові, голосні та контекстні комбінації повертають `NOT_ESTABLISHED` або `EVIDENCE_LIMITED`, а не вгадану IPA.

Профіль: `khmer-pph-careful-citation-v1`. Канонічний IPA-first конвеєр зберігає межу між фонемною нотацією Google, типізованою IPA та українською практичною адаптацією. Google-лексикон містить 62 118 непорожніх фонемних записів; усі 54 використані phone tokens присутні в зафіксованому 56-phone inventory. Це не означає, що кожне зіставлення токена з IPA є підтвердженим: 60 667 записів мають хоча б один provisional mapping, а профільна еквівалентність не ад'юдикована.

## Рівні виведення

- **Strict** — лише пропозиції рівня B з джерельними локаторами. Не використовує непідтверджені Google lexical candidates, onset-only підказки, архівні provider outputs або neural-distilled OOV.
- **Soft** — додає точні Google phonemic lexical hits та окремі IPA-підказки відомого початкового приголосного. Такі результати залишаються PROVISIONAL і завершуються `???`.
- **Super-soft** — додає детерміновані OOV-складові кандидати з таблиці, отриманої офлайновою нейромережею. Модельні ваги не надсилаються користувачу; браузер завантажує лише same-origin JSON і робить детермінований lookup. Кандидати залишаються PROVISIONAL.

Strict має найвищий доказовий поріг; Soft має ширше IPA-candidate coverage; Super-soft додає нейромережеві OOV-кандидати. Для кожного рівня окремо повертаються `tier_coverage` показники. 100% `nonempty_output_coverage` у Super-soft означає, що кожна вхідна одиниця має або кандидат, або явний unresolved marker; це **не** 100% повна IPA-транскрипція.

Орфографічний BGN/PCGN fallback лишається в окремій панелі й ніколи не підміняє IPA-derived український результат. Архівні виходи Khmer Phonemizer, MekongPhon та Epitran збережено лише для діагностики; вони не обираються як primary output. Незалежна adjudicated IPA gold вибірка наразі має 0 записів, тому незалежна вимова й точність лишаються NOT_ASSESSED.
## Python

```python
from khmer_ua import RuleBasedKhmerEngine

result = RuleBasedKhmerEngine().analyze("ខ្មែរ")
print(result["ipa"], result["ukrainian"], result["status"])
```

Сумісні назви `HybridKhmerEngine` та `create_hybrid_engine()` тепер повертають той самий правиловий рушій; ансамблювання й зовнішні backend-и видалені з цього API.


## Research-only typed external candidates

The optional Python `HybridKhmerEngine` is a separate diagnostic wrapper. It runs `RuleBasedKhmerEngine` first and preserves its final IPA/Ukrainian result. Explicitly injected providers must return structured metadata and pass through `validate_ipa_candidate`; bare strings are rejected. Candidate priority is display/execution ordering only. No provider is enabled by default and no candidate is promoted. See [hybrid API contract](hybrid-engines.md).


## Браузерне виконання без блокування інтерфейсу — 2026-11-23

Детермінований IPA-first рушій запускається в окремому Web Worker через `src/khmer-engine-client.js` та `src/khmer-engine.worker.js`. Worker імпортує локальний `convert()` із `src/khmer-engine-core.js`, не створюючи другої реалізації правил. Введений текст передається лише через локальний механізм повідомлень Worker у межах вкладки; мережевого API для обчислення немає.

Клієнт використовує той самий синхронний `convert()` як резерв, якщо Worker недоступний або повернув помилку. Ревізія рендерингу відкидає застарілі відповіді під час швидкого набору. Романізаційний шлях залишається окремим.

## Розділення рушія та UI — 2026-11-23

Детерміновану логіку винесено в `src/khmer-engine-core.js`; UI entry point залишається в `src/main.js`. Worker імпортує лише core, не підвантажуючи DOM-rendering entry point. Це зменшило Worker bundle з 136.40 до 124.02 kB у відповідних production builds. Це оптимізація складання/ізоляції та чуйності UI, а не виміряний приріст швидкості фонологічного обчислення й не нова фонологічна модель.

Перевірка точного коду head `9fd26941efb7e4936d921d700ee5215569449bda`: Quality [45136120659](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45136120659) — 453 Python tests + 70 subtests, Node checks і Vite build успішні; Chromium [45136120671](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45136120671) — 33/33, включно з реальним Worker та fallback при недоступному Worker asset.

Паритет Python↔JavaScript, tokenizer/OOV model і незалежна IPA-ад'юдикація залишаються окремими критеріями. Жодних сторонніх ваг або корпусів не додано; права на їх розповсюдження залишаються непідтвердженими.


## Перевірка гонки застарілих відповідей — 2026-11-23

Chromium-тест штучно затримує першу відповідь Worker, після чого надсилає другий ввід. Пізня перша відповідь не перезаписує новіший результат завдяки `renderRevision`. На code head `c2dc56949ee519dfcdb13139e49002b92a3fa5bc` пройшли Quality [45136544361](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45136544361) (453 Python tests + 70 subtests, Node, build) і Chromium [45136544247](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45136544247) (34/34).


## Токенізатор: паритет і швидкодія — 2026-11-23

Браузерний токенізатор синхронізовано з Python щодо Unicode 18 §16: приголосний після підрядкового незалежного голосного (приклад `ផ្ឯម`) не створює автоматичної межі. Спільні очікувані межі зберігаються в `data/tests/tokenizer-parity.json` і перевіряються тестами обох середовищ. Також перевіряються змішані Khmer/Latin, числа, пунктуація, пробіли та ZWSP.

Пошук лексичних fixture переведено на trie: найдовший fixture приймається лише тоді, коли за ним іде межа, і пошук не починається після COENG. Це прибирає повторне створення всього залишку рядка на кожній позиції.

Відтворюваний benchmark: `npm run bench:tokenizer`. GitHub Actions / Node 24, 8 000 повторених кмерських приголосних: pre-trie median 352,89 ms; trie median 4,54 ms; 77,7× у цьому синтетичному stress-тесті. Це не вимірювання повного G2P, IPA чи реального текстового навантаження. Результат на точному head `abed3d7a4d0b3c3a9e94fa48a4e50b2819194d85`: Quality [45143908134](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45143908134), Chromium [45143908115](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45143908115) — 34/34.


## Паритет притаманної голосної після підрядкового незалежного голосного — 2026-11-23

Python-рушій раніше міг вивести притаманну голосну серії для одиниці з `subscript_independent_vowels`, хоча браузерний рушій коректно утримував IPA через неповну структуру. Умова Python тепер явно забороняє такий висновок. Регресії в обох середовищах для `ផ្ឯម` підтверджують: одна орфографічна одиниця, канонічну IPA не встановлено, притаманна голосна не вгадується.

На code head `224ad5e6530596912a69b334fe98ea7329330f96` Quality [45144332414](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45144332414) — 455 Python tests + 70 subtests; Chromium [45144332627](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45144332627) — 34/34. Trie benchmark: 8 000 code points, 2,96 ms vs 223,12 ms pre-trie, 75,3×; це синтетичний токенізаторний stress-test.


## Автоматичний паритет Python↔JavaScript — 2026-11-23

Додано `data/tests/structural-parity.json` як спільний набір входів, Python reference exporter `scripts/export_structural_parity.py`, Node comparator `tests/cross-runtime-structural-parity.mjs` та CI gate `npm run test:parity`. На кожному вході звіряються токенізація й поля структури: базовий приголосний, регістр, підрядкові приголосні/незалежні голосні, залежні голосні, статус і IPA початкового приголосного.

Перший differential run знайшов розбіжність у malformed COENG: JS позначав послідовність некоректною, але втрачав уже розпізнаний базовий приголосний. Тепер структурний trace зберігає його та malformed tail, як Python. Набір із восьми випадків проходить на head `c0df000e179d6da16c05c78960ede774966bdcf7`: Quality [45145033315](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45145033315), Chromium [45145043709](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45145043709) — 34/34.

Повний семантичний паритет ще не заявляється: це початковий executable slice, який треба розширити незалежними голосними, складними кластерами, повними unit records і кінцевими IPA/UA результатами.


## Незалежні голосні в structural parity — 2026-11-23

Паритетний набір розширено до дев'яти випадків, включно з окремим незалежним голосним. JS-парсер тепер повертає його як структурно встановлену базову одиницю без приголосного регістру та onset IPA — так само, як Python. Це не є встановленням вимови.

На head `8a2d86a85436ddec149cd55a7d1909ac0b2c7cc0` пройшли Quality [45145337895](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45145337895) / [45145346826](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45145346826): 455 Python tests + 70 subtests, Node, 9-case parity, benchmark, Vite; Chromium [45145346888](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45145346888): 34/34.


## Розширення structural parity до інвентарю — 2026-11-23

Спільний корпус розширено з дев'яти прикладів до 129 випадків на основі реальних даних репозиторію: 33 приголосні, 15 незалежних голосних, залежні/композитні голосні та модифікатори, усі підрядкові приголосні й незалежні голосні, усі допустимі комбінації шифтерів та негативні структурні випадки. Python exporter і JS comparator проходять на GitHub Actions.

На head `a389530b5ffa8799b6194c939a00bce9309110e2`: Quality [45145785462](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45145785462) — 455 Python tests + 70 subtests і 129-case parity; Chromium [45145796671](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45145796671) — 34/34. Токенізаторний stress-test: 8 000 code points, 8,19 ms trie проти 490,16 ms pre-trie (59,9×); це не наскрізний G2P benchmark.

Це підтверджує паритет структурних полів на широкому інвентарі, але не повний паритет контекстної фонології, lexical/OOV word segmentation чи повного per-unit output schema.


## Підсумковий checkpoint — 2026-11-23

Поточний branch tip після оновлення документації: `f79126ae78ebcd4d5e70324c0c43736f622885b7`. Exact-tip Quality [45146037172](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45146037172): 455 Python tests + 70 subtests, Node, 129-case Python↔JS structural parity, tokenizer benchmark і Vite build — PASS. Останній code-bearing head `a389530b5ffa8799b6194c939a00bce9309110e2` пройшов Chromium [45145796671](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45145796671), 34/34; після нього були лише документаційні коміти. Benchmark на exact docs head: 8 000 code points, 2,69 ms trie vs 242,72 ms pre-trie, 90,3×; synthetic tokenizer-only stress, не повний G2P.


## Останній exact-head CI — 2026-11-23

Head `aace766c21476019952f1aa93f217396387de420`: Quality [45146465545](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45146465545) — 455 Python tests + 70 subtests, Node, 129-case Python↔JS structural parity, tokenizer benchmark і Vite build; Chromium [45146465516](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45146465516) — 34/34. Trie benchmark: 8 000 code points, 3,07 ms vs 298,09 ms pre-trie, 97,0×; лише синтетичний tokenizer stress.


## Паритет IPA та української адаптації для всіх lexical fixtures — 2026-11-23

Додано Python exporter і Node comparator, які порівнюють Python `RuleBasedKhmerEngine` та browser `convert()` для всіх 36 рядків `data/tests/web-fixtures.json`. Звіряються source alignment, IPA (знято лише браузерні обмежувальні слеші), українська адаптація, статус і lexical mapping agreement. Запис без IPA залишається withheld в обох рушіях.

На head `e584d986a7d7fe9ac177709374c29bd4298e93f2`: Quality [45147094378](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45147094378) — 455 Python tests + 70 subtests, 129 structural cases, 36 lexical fixtures, benchmark і Vite; Chromium [45147094466](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45147094466) — 34/34.


## Lexical IPA/UA parity with Python — 2026-11-23

Додано окремий executable gate `npm run test:lexical-parity`: Python `RuleBasedKhmerEngine` експортує всі записи спільного лексичного набору, Node порівнює з JS-рушієм межі одиниць, IPA, українську адаптацію, статус і `lexical_mapping_agrees`. На exact head `e584d986a7d7fe9ac177709374c29bd4298e93f2` перевірено **36/36** фікстур.

Quality [45147094378](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45147094378): 455 Python tests + 70 subtests, Node, 129 structural cases, 36 lexical fixtures, benchmark і Vite build — PASS. Chromium [45147094466](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45147094466): 34/34 — PASS.

Це не означає повної семантичної еквівалентності Python та JS або підтримки відкритого словника: перевіряються наявні спільні лексичні фікстури; загальна сегментація слів/OOV і повний result contract залишаються окремими задачами.


## Фінальний exact-head checkpoint lexical parity — 2026-11-23

Head `9a8ba02f65e0502555c0df8045e930ddcaca3a3d`: Quality [45147375553](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45147375553) — 455 Python tests + 70 subtests, Node, 129 structural cases, 36 lexical IPA/UA cases, benchmark і Vite; Chromium [45147375800](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45147375800) — 34/34. Токенізаторний stress-test цього запуску: 8 000 code points, 6,19 ms trie vs 473,60 ms pre-trie, 76,5×; синтетичне порівняння, не повний G2P.


## Бенчмарк Python↔JavaScript рушіїв — 2026-11-23

Додано `npm run bench:engine`: прогріває обидва середовища, 25 разів вимірює пакет із тих самих 36 лексичних фікстур через JS `convert()` і Python `RuleBasedKhmerEngine.analyze()`. На exact code head `bcd3421a63711812f2e9ea3533e9215796c8db59` отримано JS 0,4274 ms/36 (84 229/s) і Python 4,3880 ms/36 (8 204/s), співвідношення 10,27× на CI runner. Це мікробенчмарк конкретного набору; Python повертає багатший research result/structure контракт, а контракти JS/Python ще не повністю однакові, тому цифру не слід трактувати як чисте прискорення алгоритму або гарантію на пристроях користувачів.

Quality [45147739766](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45147739766): 455 Python tests + 70 subtests, Node, 129 structural parity, 36 lexical parity, два benchmarks, Vite build — PASS. Chromium [45147739801](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45147739801): 34/34 — PASS.


## Розширений структурний і фонологічний паритет — 2026-11-23

Structural parity тепер звіряє не лише базові поля, а й повний список grapheme trace (text/kind/codepoints), inherent-vowel series, register-shifter rule, confidence та Unicode source provenance для 129 inventory cases. Додатковий gate `npm run test:rule-parity` порівнює Python та JS виходи для 46 окремих приголосних і допустимих register-shifter форм: нормалізовану IPA, українську адаптацію, статус, rule trace, confidence tier та evidence.

На head `997a1c58dd9326d12374d9e79a73f6be5323d07d` Quality [45148673344](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45148673344): 455 Python tests + 70 subtests, 129 structural, 36 lexical і 46 rule-output parity — PASS; engine/tokenizer benchmarks та Vite build — PASS. Browser [45148673356](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45148673356) ще очікував завершення на момент запису.


## Фінальна перевірка exact tip — 2026-11-23

Branch tip `ceb249214f318f26fd35a49983fc77c9138acc61`. Quality [45148897582](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45148897582): 455 Python tests + 70 subtests, Node, 129 structural cases, 36 lexical fixtures, 46 consonant/rule-output cases, engine/tokenizer benchmarks і Vite build — PASS. Chromium [45148897606](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45148897606): 34/34 — PASS.

Same-head fixture microbenchmark: JS 0,4675 ms/36, Python 4,2747 ms/36, 9,14× на CI runner; контракти виходу ще не повністю однакові, тому це не чисте алгоритмічне порівняння. Tokenizer stress: 8 000 code points, trie 6,82 ms проти 416,37 ms pre-trie (61,1×), синтетичний tokenizer-only вимір.

Інженерна частина Worker/parity готова до review; повний проєкт лишається beta/research prototype, не release-validated за мовною точністю. OOV segmentation, повний rule/result parity та expert gold залишаються відкритими; accuracy = NOT_ASSESSED.


## Завершена перевірка rule-output parity — 2026-11-23

На head `ceb249214f318f26fd35a49983fc77c9138acc61` Quality [45148897582](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45148897582): 455 Python tests + 70 subtests, 129 structural cases з повним grapheme trace/provenance, 36 lexical IPA/UA cases, 46 consonant/register rule-output cases, обидва benchmarks і Vite build — PASS. Chromium [45148897606](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45148897606) — 34/34.

Engine microbenchmark на 36 фікстурах: JS 0,4675 ms/batch, Python 4,2747 ms/batch, 9,14× на CI runner. Python повертає багатший research contract, тому це workload-specific результат. Tokenizer stress: 8 000 code points, 3,38 ms trie vs 298,75 ms pre-trie, 88,5×; синтетичний tokenizer-only тест.


## IPA withholding parity та локальна приватність — 2026-11-23

129-case structural gate тепер також порівнює Python і JS щодо статусу та наявності/значення канонічної IPA для кожного inventory input; для PROPOSED додатково звіряється українська адаптація. Це виявляє як структурні помилки, так і помилкове встановлення IPA.

Додано Chromium regression `typing Khmer text causes no external network requests`: після завантаження сторінки ввід Khmer не має породжувати зовнішніх HTTP(S) запитів. На code head `f0f806d8f9075a92cf8faa0d0d0876e9a90b6203` пройшло 35/35 browser tests [45149575280](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45149575280).

Quality [45149642609](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45149642609) на head `338a3c0b2f941c264a3fb5f442e9b9d7156b9ee2`: 455 Python tests + 70 subtests, 129 structural/IPA, 36 lexical, 46 consonant/rule output cases, engine/tokenizer benchmarks, Vite — PASS. Engine benchmark: JS 0,4903 ms/36, Python 4,9692 ms/36, 10,13× на CI; це не чисте порівняння алгоритмів через різницю повноти результатів. Tokenizer: 3,38 ms vs 298,75 ms pre-trie, 97,7× у synthetic stress.


## IPA/status parity across the structural inventory and local-only regression — 2026-11-23

129-case structural parity тепер також викликає Python `RuleBasedKhmerEngine` і JS `convert()` для кожного випадку та порівнює кількість одиниць, статус, нормалізовану IPA (зокрема факт withholding) і український результат для PROPOSED. Це захищає від browser-only вгадування IPA для структурно відомих, але фонологічно не встановлених форм.

Додано Chromium-тест: після завантаження сторінки введення кмерського тексту не породжує жодного зовнішнього HTTP(S) запиту. Це доповнює статичний тест заборони мережевих API у Worker/client.

Quality на head `338a3c0b2f941c264a3fb5f442e9b9d7156b9ee2`: [45149642609](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45149642609) — 455 Python tests + 70 subtests, 129 structural+IPA/status, 36 lexical, 46 rule-output, benchmarks і Vite — PASS. Browser на попередньому code head [45149575280](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45149575280): 35/35, включно з no-external-request test; точний head browser workflow ще виконувався на момент запису.


## Exact final continuation tip — 2026-11-23

Branch tip `f2054dd3af325b49c5e7c87af7c90baecbf790f1`. Quality [45150128816](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45150128816): 455 Python tests + 70 subtests, Node, 129 structural+IPA/status/withholding cases, 36 lexical fixtures, 46 consonant/register rule-output cases, benchmarks and Vite — PASS. Chromium [45150129396](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45150129396): 35/35 — PASS, including local-only network regression.

Engine fixture microbenchmark: JS 0,4859 ms/36, Python 4,9776 ms/36, observed 10,24× on CI; not a controlled algorithm-only comparison. Tokenizer stress: 8 000 code points, trie 6,23 ms vs 466,28 ms pre-trie (74,9×), synthetic tokenizer-only result.


## Typed IPA result and single target adapter — 2026-11-24

The deterministic Khmer engine now exposes a typed IPA boundary that mirrors the Lao engine's result architecture without importing Lao phonological rules or source values.

### Typed result model

- `TypedPhoneticResult` contains `phonemic_ipa`, inspectable `segments`, `syllable_boundaries`, `vowel_length`, explicit tone slots, `status`, `provenance` and `uncertainty`.
- Each `PhoneticSegment` retains its IPA text, segment kind, provenance and certainty.
- Typed statuses are `SUPPORTED`, `UNCERTAIN`, `PROVISIONAL` and `UNRESOLVED`. The existing Khmer engine statuses are unchanged and remain a separate dimension.
- Current source-attested lexical IPA proposals map to nested `UNCERTAIN`, not `SUPPORTED`; no adjudicated gold exists to justify the latter.
- Registered onset-only hints map to `PROVISIONAL`, have `phonemic_ipa=null`, and always carry one explicit unresolved tail.
- No hint maps to `UNRESOLVED` and `???`.

### One IPA-only target boundary

Python `adapt_phonetic_result()` and browser `adaptPhoneticResult()` consume only typed IPA. Complete and provisional phonetic output use this same adapter. The IPA parser is independent of the Ukrainian correspondence table; a valid IPA sequence remains `UNCERTAIN` even when the target adapter cannot map it. Such cases do not trigger a guessed Ukrainian output.

The adapter never reads Khmer graphemes, source positions or romanization. The separate BGN/PCGN orthographic candidate remains `ORTHOGRAPHIC_ROMANIZATION_FALLBACK`, with its own provenance, and is never fed to the IPA adapter. External providers remain opt-in and non-canonical.

### Preserved features and display

IPA segments retain syllable boundaries, vowel length, tone symbols, certainty, provenance and uncertainty. Tone is not inferred by this change; tone fields remain null for Khmer unless an accepted source explicitly supplies them. Unknown regions render as a single `???` per contiguous region. The browser unit detail and CLI expose the typed status and uncertainty.

Exact-head Quality [45490428639](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45490428639) passed 503 Python tests + 70 subtests, web checks, parity, benchmark and production build. Chromium [45490428728](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45490428728) passed 42/42 Playwright tests; pinned Rust segmentation [45490428786](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45490428786) and external khPOS [45490428814](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45490428814) also passed. This engineering contract does not increase phonological evidence coverage or establish pronunciation accuracy.

## Нейромережева дистиляція в локальний детермінований рушій — 2026-11-25 (PR #582)

### Архітектура

`ліцензований кмерський фонемний корпус → офлайнова нейромережева модель-вчитель → перевірена статична таблиця кандидатів → локальний детермінований рушій → типізований IPA → український IPA-адаптер`.

Нейромережа використовується під час розробки/збирання, а не під час роботи сайту. Відвідувач не завантажує ваги моделі й не запускає ONNX. Браузерний рушій працює через локальний Web Worker із детермінованими правилами, локальним фонемним лексиконом і статичною таблицею кандидатів; резервний шлях використовує ті самі локальні дані. Кмерський текст не надсилається на зовнішній сервіс.

### Джерело й фонемний адаптер

- Google Khmer pronunciation TSV зафіксований на commit `a90601024f07ab7e96c911243324e0adeb16da96`; сам TSV оголошує CC BY 4.0. Companion Festvox phonology JSON має невирішений scope ліцензії й не копіюється/не поширюється. Runtime-мапа перевіряється безпосередньо за 54 токенами ліцензованого TSV.
- У корпусі 62,118 непорожніх кмерських фонемних рядків, 61 порожній рядок, 62,114 унікальних написань і чотири написання з кількома варіантами. Усі 54 фактично вживані токени присутні в інвентарі з 56 фонем.
- Google-нотація не є IPA. `src/khmer_ua/google_phonemic.py` і `src/google-phonemic-ipa.js` виконують окреме типізоване перетворення. Межі складів, довгота, вихідні токени, ревізія, рядок TSV і статуси мапування зберігаються.
- Невідомі, порожні та нефонемні токени не вгадуються. Кілька вимов одного написання лишаються кількома кандидатами; порожні джерельні рядки лишаються невстановленими.
- Усі українські фонетичні форми проходять лише через спільний IPA → український адаптер.

### Навчання й дистиляція

- Проєкт має власну офлайнову seq2seq-модель-вчитель, навчену на закріпленому корпусі з поділом train/dev/test за нормалізованим написанням. Токени фонем є атомарними; `ph`, `aa`, `ie` не розбиваються на символи.
- На held-out Google source labels: 84,18% word exact, 4,33% phoneme-token error rate, 100% label coverage. Це прогнозування міток корпусу, а не IPA accuracy.
- Скрипт дистиляції генерує 2,532 OOV-складові кандидати. На діагностиці композиції: 63,86% exact, 14,19% token error rate, 98,4% coverage за припущенням про відповідність кількості орфографічних і фонологічних складів.
- Кожен дистильований кандидат має статус PROVISIONAL. Збіг із власним teacher не є незалежним підтвердженням і не може сам по собі підвищити правило до SUPPORTED.
- Таблиця в браузері — статичний JSON; модельний checkpoint залишається артефактом дослідження/збирання. Вона завантажується same-origin лише для Super-soft.

### Рівні результату

- **Strict**: лише пропозиції з допустимою джерельною опорою; неперевірені Google і нейродистильовані кандидати не підміняють канонічний результат.
- **Soft**: може показати точний збіг у локальному фонемному словнику як PROVISIONAL-кандидат, зберігаючи невизначеність і окрему орфографічну підказку.
- **Super-soft**: додатково використовує статичні нейродистильовані складові кандидати. Відсутність повного кандидата не приховується; доступний onset-only або явний маркер невизначеності.
- Гарантія 100% для Super-soft стосується непорожнього відображуваного результату, а не 100% повної IPA-транскрипції. Повна IPA coverage, partial coverage, unresolved coverage та display coverage мають рахуватися окремо.
- Вимога Strict accuracy > Soft > Super-soft іще не перевірена: незалежний ад'юдикований IPA gold corpus має 0 записів. Профільна еквівалентність Google-нотації до `khmer-pph-careful-citation-v1` також UNVERIFIED.

### Відкинуті teacher-кандидати

- MekongPhon greedy і beam-4 дали 0/6 точних збігів та 44,44% codepoint CER на вузькій source-attested матриці. Це не accuracy, але gate не пройдено; модель не обрана teacher для дистиляції.
- NCKL split-syllable respelling → Khmer Phonemizer дав 8/12 exact і 6,93% CER; whole-string і spaced-string варіанти кожен дали 7/12 exact і 6,93% CER. Прямий Khmer Phonemizer на тому самому наборі дав 11/12 exact і 0,99% CER. Жоден NCKL bridge не інтегровано.
- Обидва результати залишаються негативними діагностичними контрольними точками, а не причиною видаляти сторонні дослідження.

### Поточний стан перевірки

- Попередній повний Quality/teacher/distillation run [45653367069](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45653367069) пройшов на своєму exact head.
- Пізніші browser smoke запуски виявили застарілі тестові очікування щодо canonical unresolved marker і provenance, а також реальну помилку UI: локальний Google-кандидат називався зовнішнім провайдером. Тести оновлено; `getStatusNotice` виправлено в commit `755a89c695e93594adb3c980f2cc87adde80f6fd`.
- Exact-head Quality, Chromium та benchmark перевірки після останнього коду й документаційних комітів мають бути завершені на одному SHA. До цього рушій не оголошується release-ready.
