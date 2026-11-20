import report from "../reports/khmer-coverage-audit.json" with { type: "json" };

const labels = {
  SOURCE_ATTESTED_NOT_GOLD: "Є приклад з джерела · не еталон",
  CONFLICTING_SOURCE_ANALYSES: "Конфлікт джерел",
  NOT_ESTABLISHED: "Не встановлено",
};

const summary = document.querySelector("#coverage-summary");
const rows = document.querySelector("#coverage-rows");
const conflictBox = document.querySelector("#coverage-conflicts");
const contextRows = document.querySelector("#coverage-context-rows");

function element(tag, className, text) {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (text !== undefined) node.textContent = String(text);
  return node;
}

function renderSummary() {
  const inventory = report.orthographic_inventory;
  const counts = report.coverage_summary;
  const cards = [
    ["Комірок", inventory.expected_dependent_vowel_x_series_cells],
    ["Прикладів із джерел", counts.source_attested_not_gold_cells],
    ["Не встановлено", counts.not_established_cells],
    ["Конфліктних комірок", counts.conflicting_cells],
  ];
  summary.replaceChildren();
  for (const [label, value] of cards) {
    const card = element("div", "coverage-stat");
    card.append(element("span", "", label), element("strong", "", value));
    summary.append(card);
  }
  summary.append(element(
    "p",
    "coverage-warning",
    "Це інвентар наявних свідчень, а не відсоток фонетичної точності. Повнота контекстної матриці ще не досягнута.",
  ));
}

function renderRows() {
  rows.replaceChildren();
  for (const cell of Object.values(report.dependent_vowel_by_series)) {
    const row = document.createElement("tr");
    row.append(
      element("td", "coverage-sign", cell.sign),
      element("td", "coverage-code", cell.codepoint),
      element("td", "", cell.series === "first" ? "Перша" : "Друга"),
    );
    const status = element("span", `coverage-status ${cell.status.toLowerCase().replaceAll("_", "-")}`, labels[cell.status] ?? cell.status);
    const statusCell = document.createElement("td");
    statusCell.append(status);
    row.append(statusCell);
    row.append(element("td", "coverage-ipa", cell.ipa_values.join(" · ") || "—"));
    row.append(element("td", "coverage-cases", cell.case_ids.filter(Boolean).join(", ") || "—"));
    rows.append(row);
  }
}


function markerText(value) {
  if (Array.isArray(value)) return value.filter(item => item !== null && item !== "").join(" · ") || "—";
  return value === null || value === undefined || value === "" ? "—" : String(value);
}

function lengthLabel(value) {
  if (value === "EXPLICIT_LENGTH_MARK_IN_SOURCE_TRANSCRIPTION") return "Є позначка довготи в джерелі";
  if (value === "NO_EXPLICIT_LENGTH_MARK_SHORTNESS_NOT_INFERRED") return "Позначки немає; короткість не виводимо";
  return "Не встановлено";
}

function renderContextRows() {
  if (!contextRows) return;
  contextRows.replaceChildren();
  for (const item of report.contextual_vowel_evidence?.observations ?? []) {
    const row = document.createElement("tr");
    row.append(
      element("td", "coverage-code", item.case_id),
      element("td", "coverage-sign", item.orthography),
      element("td", "", item.base_consonant_class === "first" ? "Перша" : item.base_consonant_class === "second" ? "Друга" : "Не встановлено"),
      element("td", "coverage-sign", item.dependent_vowel_sequence.join(" · ") || "—"),
      element("td", "coverage-code", markerText(item.orthographic_coda_marker)),
      element("td", "coverage-ipa", item.source_transcription || "—"),
    );
    const evidence = document.createElement("td");
    const status = element(
      "span",
      `coverage-status ${String(item.evidence_status).toLowerCase().replaceAll("_", "-")}`,
      labels[item.evidence_status] ?? item.evidence_status,
    );
    evidence.append(status, element("div", "coverage-length", lengthLabel(item.length_evidence)));
    row.append(evidence);
    contextRows.append(row);
  }
}

function renderConflicts() {
  conflictBox.replaceChildren();
  conflictBox.append(element("b", "", "Конфлікти та обмеження"));
  const ids = report.source_conflict_case_ids;
  conflictBox.append(element(
    "span",
    "",
    ids.length
      ? `Зареєстровані конфлікти поза цією вузькою матрицею: ${ids.join(", ")}. Вони не були зведені до однієї IPA-відповідності.`
      : "У поточному джерельному реєстрі конфліктних прикладів не зафіксовано.",
  ));
  conflictBox.append(element(
    "span",
    "",
    "Відсутність доказів не означає відсутність фонологічного правила; вона означає, що його не можна безпечно вивести з наявних записів.",
  ));
}

if (summary && rows && conflictBox) {
  renderSummary();
  renderRows();
  renderContextRows();
  renderConflicts();
}
