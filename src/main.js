import fixtures from "../data/tests/web-fixtures.json" with { type: "json" };
import { khmerToLatin } from "@gmana/km-translit";
import { renderKhmerRomanizationText, renderRomanizedText } from "./khmer-romanization-ukrainian.js";
import { analyzeInWorker } from "./khmer-engine-client.js";
import { convert, getStatusNotice } from "./khmer-engine-core.js";

if (typeof document !== "undefined") {
  const $ = (id) => document.getElementById(id);
  const source = $("source");
  const romanizationResult = $("romanization-result");
  const results = $("results");
  const empty = $("empty");
  const issue = $("issue");
  const live = $("live");
  const modePhonetic = $("mode-phonetic");
  const modeRomanization = $("mode-romanization");
  const outputMethodNote = $("output-method-note");
  const uaResultTitle = $("ua-result-title");
  const uaResultDescription = $("ua-result-description");
  const outputLevel = $("output-level");
  const outputLevelNote = $("output-level-note");
  let outputLevelMode = outputLevel?.value || "balanced";
  let activeMode = "phonetic";
  let renderRevision = 0;

  function setOutputMode(mode) {
    activeMode = mode;
    document.querySelectorAll("[data-method-panel]").forEach((panel) => {
      panel.hidden = panel.dataset.methodPanel !== mode;
    });
    modePhonetic.classList.toggle("is-active", mode === "phonetic");
    modePhonetic.setAttribute("aria-pressed", String(mode === "phonetic"));
    modeRomanization.classList.toggle("is-active", mode === "romanization");
    modeRomanization.setAttribute("aria-pressed", String(mode === "romanization"));
    outputMethodNote.textContent = mode === "phonetic"
      ? "Шлях 1 · за вимовою: кмерська графіка → структурний і фонологічний аналіз → IPA → українська адаптація. Невстановлені IPA-фрагменти залишаються явно позначеними."
      : "Шлях 2 · з романізації: кмерська графіка → BGN/PCGN-derived латинський запис або готова BGN/PCGN-форма → українська орфографічна передача. Це не фонетична транскрипція; IPA тут не використовується.";
    uaResultTitle.textContent = mode === "phonetic" ? "Українська за вимовою (IPA)" : "Українська з романізації";
    uaResultDescription.textContent = mode === "phonetic"
      ? "Результат проходить через IPA та українську фонетичну адаптацію."
      : "Окремий орфографічний шлях через BGN/PCGN; не залежить від стану IPA.";
    render();
  }

  async function render() {
    const revision = ++renderRevision;
    const inputText = source.value;
    const profile = $("profile").value;
    $("count").textContent = `${[...inputText].length} символів`;
    const data = await analyzeInWorker(inputText, profile, convert);
    if (revision !== renderRevision) return;
    if (!data) {
      results.hidden = true;
      issue.hidden = true;
      empty.hidden = false;
      return;
    }
    empty.hidden = true;
    results.hidden = false;
    const hasKhmer = [...data.source].some(char => /\p{Script=Khmer}/u.test(char) && /[\p{L}\p{M}]/u.test(char));
    const hasLatin = /\p{Script=Latin}/u.test(data.source);
    const hasMixedScript = hasKhmer && hasLatin;
    const usesKhmerRomanizer = hasKhmer && !hasLatin;
    const latinRomanization = usesKhmerRomanizer ? khmerToLatin(data.source) : data.source;
    romanizationResult.textContent = latinRomanization;
    const uaRomanized = usesKhmerRomanizer
      ? renderKhmerRomanizationText(data.source, khmerToLatin)
      : renderRomanizedText(data.source);
    $("romanization-title").textContent = hasMixedScript
      ? "Змішаний ввід · потрібен один формат"
      : usesKhmerRomanizer
        ? "Романізація · BGN/PCGN-derived ASCII"
        : "Вхідна романізація · BGN/PCGN 1972";
    $("romanization-description").textContent = hasMixedScript
      ? "Одночасний кмерський і латинський текст не підтримується як один профіль; кмерські літери позначено."
      : usesKhmerRomanizer
        ? "Автоматичний латинський запис із кмерського письма; не IPA."
        : "Готовий латинський запис обробляється без повторної романізації.";
    $("romanization-note").textContent = hasMixedScript
      ? "Розділіть кмерський текст і BGN/PCGN-романізацію на окремі запуски."
      : usesKhmerRomanizer
        ? "Пакет @gmana/km-translit 0.1.2 відкидає діакритики BGN/PCGN; контекстні голосні не можна відновити однозначно."
        : "Діакритичні форми BGN/PCGN підтримуються за таблицею; невідомі латинські фрагменти залишаються в ⟦…⟧. Українські відповідники — проєктні кандидати.";
    $("ua-romanization-result").textContent = uaRomanized.text || "—";
    $("ua-romanization-status").textContent = uaRomanized.status === "PROVISIONAL"
      ? usesKhmerRomanizer
        ? "PROVISIONAL · буквена передача з ASCII-результату; пакет відкидає BGN/PCGN діакритики, тому контекстні голосні не можна відновити однозначно."
        : "PROVISIONAL · пряма передача з BGN/PCGN-романізації; українські відповідники мають статус проєктних кандидатів."
      : uaRomanized.status === "PARTIAL"
        ? "PARTIAL · зіставлено " + uaRomanized.mapped + " фрагм.; " + uaRomanized.unsupported + " непідтримуваних фрагм. позначено в ⟦…⟧."
        : "PASSTHROUGH · латинських фрагментів для романізації немає; сторонній текст збережено.";
    const romanizationOnlyInput = hasLatin && !hasKhmer;
    // A Latin BGN/PCGN input is already romanized: do not send it through the
    // Khmer orthography parser and then present its expected abstention as the
    // primary result. Route it to the separate orthographic UA renderer.
    $("ipa-result").textContent = romanizationOnlyInput
      ? "— · IPA не застосовується до готової романізації"
      : data.ipa;
    const moveMarkerToWordEnd = (value) => String(value || "").split(/(\s+)/u)
      .map((part) => {
        if (/^\s+$/u.test(part) || !part || !part.includes("???")) return part;
        const candidate = part.split("???").join("");
        if (!candidate) return "???";
        const chars = Array.from(candidate);
        const firstNumber = chars.findIndex((char) => /\p{N}/u.test(char));
        return firstNumber < 0
          ? candidate + "???"
          : chars.slice(0, firstNumber).join("") + "???" + chars.slice(firstNumber).join("");
      }).join("");
    // The primary phonetic field is IPA-derived only. Orthographic romanization
    // is available exclusively after the user selects its independent route.
    const phoneticUaOutput = romanizationOnlyInput
      ? "— · для готової романізації оберіть метод «З романізації»"
      : moveMarkerToWordEnd(data.ua);
    const romanizationUaOutput = uaRomanized.text || "???";
    $("ua-result").textContent = activeMode === "romanization"
      ? romanizationUaOutput
      : phoneticUaOutput;
    $("status").textContent = activeMode === "romanization"
      ? romanizationOnlyInput
        ? "РОМАНІЗАЦІЯ · ВХІД УЖЕ ЛАТИНКОЮ · " + uaRomanized.status
        : "РОМАНІЗАЦІЯ · BGN/PCGN-DERIVED · " + uaRomanized.status
      : romanizationOnlyInput
        ? "IPA НЕ ЗАСТОСОВУЄТЬСЯ ДО ГОТОВОЇ РОМАНІЗАЦІЇ"
        : data.selected_external_candidate
          ? "EXTERNAL IPA CANDIDATE · " + data.selected_external_candidate.provider + " · PROFILE MATCH UNVERIFIED · ??? наприкінці неперевіреного результату · доказовий рівень C"
          : data.status.replaceAll("_", " ") + " · доказовий рівень " + data.confidence_tier;
    const levelGuidance = {
      strict: "Обережний рівень: показано лише наявні джерельно індексовані пропозиції; непідтверджені IPA/українські форми не реконструюються. PROPOSED не є експертним gold.",
      balanced: "Збалансований рівень: показує основний частковий результат, статус кожної одиниці та причини невизначеності. Невстановлені фрагменти зберігаються на своїх позиціях.",
      exploratory: "Дослідницький рівень: додатково показує доступні часткові структурні підказки початкового приголосного. Вони не є повним складом, IPA або підтвердженою українською вимовою."
    };
    outputLevelNote.textContent = levelGuidance[outputLevelMode];
    $("details").textContent = data.note + " " + levelGuidance[outputLevelMode];
    const unitDetails = $("unit-details");
    unitDetails.replaceChildren();
    const unitHeading = document.createElement("h3");
    unitHeading.textContent = "Одиничний аналіз";
    unitDetails.append(unitHeading);
    data.units.filter((unit) => unit.status !== "PUNCTUATION").forEach((unit) => {
      const card = document.createElement("article");
      card.className = "unit-detail";
      card.dataset.fallbackRuleId = unit.fallback_trace?.[0]?.rule_id ?? "";
      card.dataset.fallbackPosition = unit.fallback_trace?.[0]?.position ?? "";
      const heading = document.createElement("div");
      heading.className = "unit-detail-heading";
      const sourceLabel = document.createElement("strong");
      sourceLabel.className = "unit-source";
      sourceLabel.lang = "km";
      sourceLabel.textContent = unit.source;
      const statusLabel = document.createElement("span");
      statusLabel.className = "unit-status";
      statusLabel.textContent = unit.status.replaceAll("_", " ") + " · рівень " + unit.confidence_tier;
      heading.append(sourceLabel, statusLabel);
      const values = document.createElement("p");
      values.className = "unit-values";
      values.textContent = "IPA: " + unit.ipa
        + (unit.fallback_status === "PROVISIONAL"
          ? " · Попередня українська форма: " + unit.fallback_ukrainian + " [PROVISIONAL · BGN/PCGN, не IPA]"
          : " · Українська: " + unit.ua)
        + (unit.provisional_ipa ? " · Попередня підказка: " + unit.provisional_ipa + " → " + unit.provisional_ukrainian + " [PROVISIONAL]" : "");
      const note = document.createElement("p");
      note.className = "unit-note";
      note.textContent = unit.note || "Окремого пояснення для цієї одиниці немає.";
      card.append(heading, values, note);
      if (outputLevelMode === "exploratory") {
        const parts = unit.analysis?.orthographic_structure?.components ?? unit.analysis?.graphemes ?? [];
        if (parts.length) {
          const structure = document.createElement("p");
          structure.className = "unit-note";
          structure.textContent = "Розпізнана графемна структура: " + parts.map((part) => {
            const role = part.role ?? part.kind ?? "елемент";
            const status = part.status && part.status !== "RECOGNIZED" ? " (" + part.status + ")" : "";
            return role + " «" + part.text + "»" + status;
          }).join(" · ");
          card.append(structure);
        }
      }
      if (unit.source_locator) {
        const locator = document.createElement("p");
        locator.className = "unit-source-locator";
        locator.textContent = "Джерельний локатор: " + unit.source_locator;
        card.append(locator);
      }
      unitDetails.append(card);
    });
    const segmentation = data.word_segmentation;
    if (segmentation?.candidate_runs?.length) {
      const segmentationHeading = document.createElement("h3");
      segmentationHeading.textContent = "Кандидатні межі слів · альтернативні шляхи";
      unitDetails.append(segmentationHeading);
      const segmentationNote = document.createElement("p");
      segmentationNote.className = "unit-note";
      segmentationNote.textContent = segmentation.score_note
        + " Вартість нижча — шлях краще відповідає частотній моделі; це не ймовірність і не оцінка мовної правильності.";
      unitDetails.append(segmentationNote);
      segmentation.candidate_runs.forEach((run) => {
        const runCard = document.createElement("article");
        runCard.className = "unit-detail";
        const runTitle = document.createElement("strong");
        runTitle.className = "unit-source";
        runTitle.lang = "km";
        runTitle.textContent = run.source;
        runCard.append(runTitle);
        run.chunks.forEach((chunk) => {
          const chunkTitle = document.createElement("p");
          chunkTitle.className = "unit-note";
          chunkTitle.lang = "km";
          chunkTitle.textContent = chunk.method === "LEXICAL_FIXTURE_PROTECTED"
            ? "Захищена лексична одиниця: " + chunk.source
            : chunk.method === "DIAGNOSTICS_SKIPPED_LENGTH_LIMIT"
              ? "Додаткові варіанти пропущено: понад 128 кластерів; основна сегментація не змінена."
              : "Фрагмент для словникового пошуку: " + chunk.source;
          runCard.append(chunkTitle);
          if (chunk.method !== "LEXICAL_FIXTURE_PROTECTED") chunk.candidates.forEach((candidate) => {
            const candidateLine = document.createElement("p");
            candidateLine.className = "unit-values";
            const rendered = candidate.segments.map((segment) =>
              segment.text + (segment.status === "OOV_RUN" ? " [OOV]" : "")
            ).join(" | ");
            candidateLine.textContent = "Варіант " + candidate.rank + ": " + rendered
              + " · вартість моделі " + candidate.cost.toFixed(4);
            runCard.append(candidateLine);
          });
        });
        unitDetails.append(runCard);
      });
    }
    if (data.external_candidates?.length) {
      const providerHeading = document.createElement("h3");
      providerHeading.textContent = "Зовнішні IPA-кандидати · не перевірені";
      unitDetails.append(providerHeading);
      data.external_candidates.forEach((candidate) => {
        const card = document.createElement("article");
        card.className = "unit-detail";
        const heading = document.createElement("div");
        heading.className = "unit-detail-heading";
        const provider = document.createElement("strong");
        provider.textContent = candidate.provider + (candidate.selected ? " · вибраний для попереднього показу" : "");
        const status = document.createElement("span");
        status.className = "unit-status";
        status.textContent = candidate.status + " · profile match " + candidate.profile_match;
        heading.append(provider, status);
        const values = document.createElement("p");
        values.className = "unit-values";
        values.textContent = "IPA: /" + candidate.ipa + "/???"
          + (candidate.mapped_ukrainian
            ? " · Українське зіставлення: " + candidate.mapped_ukrainian + "???"
            : " · Українське зіставлення: не отримано" + (candidate.mapping_failure ? " · непідтриманий фрагмент: " + candidate.mapping_failure : ""));
        const provenance = document.createElement("p");
        provenance.className = "unit-note";
        provenance.textContent = "Походження: " + JSON.stringify(candidate.provenance)
          + " · Невизначеність: " + (candidate.uncertainty || []).join(" ");
        card.append(heading, values, provenance);
        unitDetails.append(card);
      });
    }
    if (data.backend_failures?.length) {
      const failureHeading = document.createElement("h3");
      failureHeading.textContent = "Відхилені виходи провайдерів";
      unitDetails.append(failureHeading);
      data.backend_failures.forEach((failure) => {
        const item = document.createElement("p");
        item.className = "unit-note";
        item.textContent = failure.provider + ": " + failure.reason
          + (failure.raw_output ? " · raw output: " + failure.raw_output : "");
        unitDetails.append(item);
      });
    }
    unitDetails.hidden = activeMode !== "phonetic" || outputLevelMode === "strict" || (data.units.every((unit) => unit.status === "PUNCTUATION") && !data.external_candidates?.length);
    const notice = getStatusNotice(data);
    issue.hidden = activeMode !== "phonetic" || !notice;
    if (!issue.hidden) {
      $("issue-text").textContent = notice;
      $("issue").querySelector("strong").textContent =
        data.status === "PROPOSED" ? "Результат попередній" : "Результат потребує обережності";
    }
    live.textContent = "Результат оновлено";
  }
  
  modePhonetic.addEventListener("click", () => setOutputMode("phonetic"));
  modeRomanization.addEventListener("click", () => setOutputMode("romanization"));
  setOutputMode("phonetic");
  source.addEventListener("input", render);
  outputLevel?.addEventListener("change", () => { outputLevelMode = outputLevel.value; render(); });
  $("profile").addEventListener("change", render);
  $("example").addEventListener("click", () => {
    source.value = fixtures["ភាសាខ្មែរ"] ? "ភាសាខ្មែរ" : Object.keys(fixtures)[0];
    render();
    source.focus();
  });
  $("clear").addEventListener("click", () => {
    source.value = "";
    render();
    source.focus();
  });
  document.querySelectorAll("[data-copy]").forEach((button) => {
    button.addEventListener("click", async () => {
      const element = $(button.dataset.copy);
      try {
        const copyText = "value" in element ? element.value : element.textContent;
        await navigator.clipboard.writeText(copyText);
        const old = button.textContent;
        button.textContent = "Скопійовано";
        window.setTimeout(() => { button.textContent = old; }, 900);
      } catch {
        live.textContent = "Не вдалося скопіювати автоматично. Виділіть результат і скопіюйте вручну.";
      }
    });
  });
  
}
