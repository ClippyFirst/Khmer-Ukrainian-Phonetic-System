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

Детермінований IPA-first рушій тепер запускається в окремому Web Worker через `src/khmer-engine-client.js` та `src/khmer-engine.worker.js`. Worker імпортує той самий локальний `convert()` із `src/khmer-engine-core.js`, тому не створює другої реалізації правил і не змінює семантику IPA/українського результату. Мережевих запитів для обчислення немає; текст передається лише між головним потоком і Worker у межах вкладки.

Клієнт використовує локальний синхронний `convert()` як fail-safe, якщо Worker недоступний або повернув помилку. Номер ревізії рендерингу відкидає застарілі відповіді при швидкому наборі тексту. Романізаційний шлях лишається окремим і не підміняє IPA-first фонетичний рушій.

Це оптимізація чуйності інтерфейсу, а не нова фонологічна модель і не доказ точності. Паритет Python↔JavaScript, ширше покриття та незалежна експертна IPA-ад'юдикація залишаються окремими критеріями.


### Engine/UI module separation — 2026-11-23

The deterministic engine has been extracted into `src/khmer-engine-core.js`. The UI entry point `src/main.js` now imports only the functions it needs, while the Worker imports the core directly and no longer bundles the DOM-rendering entry point. Runtime, register-shifter and structural tests now import the core module; static source guards inspect both core and UI where appropriate. The core retains the existing deterministic rules and local romanization-derived fallback dependency; this is modularization, not a new phonology model.
