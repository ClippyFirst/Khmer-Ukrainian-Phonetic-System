# Детермінований кмерський рушій

Активний браузерний рушій і Python API працюють за фіксованими правилами. Вони не запускають нейромережі, не звертаються до мережі, не викликають сторонні G2P-процеси й не голосують між кандидатами.

## Конвеєр

1. NFC-нормалізація та сегментація кмерського письма.
2. Структурний розбір приголосних, підрядкових знаків, голосних і регістрових маркерів.
3. Для лексичних винятків — точний пошук у версійованому наборі засвідчених прикладів.
4. Для вузького класу підтриманих структур — застосування явного правила серії та притаманного голосного.
5. Перевірка IPA → українська за найдовшим точним збігом у канонічній таблиці.

## Детермінованість і межі

Однаковий нормалізований ввід, версія правил і набір даних дають однаковий результат. Це властивість обчислення, а не автоматичний доказ фонетичної істинності. Статус `PROPOSED` залишається запропонованим; непідтримані підрядкові, голосні та контекстні комбінації повертають `NOT_ESTABLISHED` або `EVIDENCE_LIMITED`, а не вгадану IPA.

Профіль: `khmer-pph-careful-citation-v1`. Основний IPA-first розрахунок не бере романізацію за джерело фонетичних фактів. Якщо IPA для одиниці не встановлено, але наявний BGN/PCGN-derived romanizer може її відобразити, інтерфейс автоматично показує її українську орфографічну адаптацію як `PROVISIONAL` кандидат на всіх рівнях деталізації — без перемикання режимів і без `???` після доступного кандидата. Це не IPA-вимова і не змінює IPA або per-unit phonetic status (`NOT_ESTABLISHED` залишається в аналізі). Машинне поле `ukrainian_kind` розрізняє `ORTHOGRAPHIC_ROMANIZATION_FALLBACK` і IPA-derived adaptation. Некоректні або непідтримувані фрагменти, для яких немає повного кандидата, зберігають локальний `???`.

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
