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
