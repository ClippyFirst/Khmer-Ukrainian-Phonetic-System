import { test, expect } from "@playwright/test";

test("Khmer input renders IPA and Ukrainian output without a DOM exception", async ({ page }) => {
  const pageErrors = [];
  page.on("pageerror", error => pageErrors.push(error.message));
  await page.goto("/");
  await page.locator("#source").fill("ក");
  await expect(page.locator("#results")).toBeVisible();
  await expect(page.locator("#ipa-result")).toHaveText("/kɑː/");
  await expect(page.locator("#ua-result")).toHaveText("ка");
  await expect(page.locator("#status")).toHaveText("PROPOSED");
  expect(pageErrors).toEqual([]);
});

test("unsupported mixed input remains visibly withheld", async ({ page }) => {
  await page.goto("/");
  await page.locator("#source").fill("កx");
  await expect(page.locator("#results")).toBeVisible();
  await expect(page.locator("#status")).toHaveText("INVALID OR UNSUPPORTED");
  await expect(page.locator("#ua-result")).toHaveText("⟦ТРАНСКРИПЦІЮ НЕ ВСТАНОВЛЕНО ДЛЯ ЧАСТИНИ ВВОДУ⟧");
});

test("clear control restores the empty state", async ({ page }) => {
  await page.goto("/");
  await page.locator("#source").fill("ក");
  await page.locator("#clear").click();
  await expect(page.locator("#results")).toBeHidden();
  await expect(page.locator("#empty")).toBeVisible();
});

test("romanization mode renders a separate provisional Ukrainian form", async ({ page }) => {
  await page.goto("/");
  await page.locator("#source").fill("សុខា");
  await page.locator("#mode-romanization").click();
  await expect(page.locator("#romanization-result")).toHaveText("Sokha");
  await expect(page.locator("#ua-romanization-result")).toHaveText("Сок'а");
  await expect(page.locator("#ua-romanization-status")).toContainText("PROVISIONAL");
  await expect(page.locator("#ipa-result")).toBeHidden();
});


test("pre-romanized BGN/PCGN input maps directly to Ukrainian with diacritics", async ({ page }) => {
  await page.goto("/");
  await page.locator("#source").fill("Kâmpŭchéa");
  await page.locator("#mode-romanization").click();
  await expect(page.locator("#romanization-result")).toHaveText("Kâmpŭchéa");
  await expect(page.locator("#ua-romanization-result")).toHaveText("Кампучеа");
  await expect(page.locator("#ua-romanization-status")).toContainText("PROVISIONAL");
  await expect(page.locator("#romanization-title")).toHaveText("Вхідна романізація · BGN/PCGN 1972");
  await expect(page.locator("#ipa-result")).toBeHidden();
});

test("unknown pre-romanized fragments are bracketed, not guessed", async ({ page }) => {
  await page.goto("/");
  await page.locator("#source").fill("Kâmpŭchéa q");
  await page.locator("#mode-romanization").click();
  await expect(page.locator("#ua-romanization-result")).toHaveText("Кампучеа ⟦q⟧");
  await expect(page.locator("#ua-romanization-status")).toContainText("PARTIAL");
});


test("phonetic diagnostics stay hidden while editing direct romanization input", async ({ page }) => {
  await page.goto("/");
  await page.locator("#source").fill("Kâmpŭchéa");
  await page.locator("#mode-romanization").click();
  await page.locator("#source").fill("Kâmpŭchéa q");
  await expect(page.locator("#ua-romanization-result")).toHaveText("Кампучеа ⟦q⟧");
  await expect(page.locator("#issue")).toBeHidden();
  await expect(page.locator("#unit-details")).toBeHidden();
});


test("mixed Khmer letters in direct romanization mode are bracketed as unsupported", async ({ page }) => {
  await page.goto("/");
  await page.locator("#source").fill("Kâmpŭchéa ខ្មែរ");
  await page.locator("#mode-romanization").click();
  await expect(page.locator("#ua-romanization-result")).toHaveText("Кампучеа ⟦ខ⟧⟦្⟧⟦ម⟧⟦ែ⟧⟦រ⟧");
  await expect(page.locator("#ua-romanization-status")).toContainText("PARTIAL");
  await expect(page.locator("#romanization-title")).toHaveText("Змішаний ввід · потрібен один формат");
  await expect(page.locator("#romanization-note")).toContainText("окремі запуски");
});


test("Khmer numerals do not incorrectly trigger the mixed-script warning", async ({ page }) => {
  await page.goto("/");
  await page.locator("#source").fill("Kâmpŭchéa ២០២៦។");
  await page.locator("#mode-romanization").click();
  await expect(page.locator("#ua-romanization-result")).toHaveText("Кампучеа 2026។");
  await expect(page.locator("#ua-romanization-status")).toContainText("PROVISIONAL");
  await expect(page.locator("#romanization-title")).toHaveText("Вхідна романізація · BGN/PCGN 1972");
});


test("primary input and method controls expose accessible names", async ({ page }) => {
  await page.goto("/");
  await expect(page.getByRole("textbox", { name: "Введіть кмерський текст або латинську романізацію BGN/PCGN 1972" })).toBeVisible();
  await page.locator("#source").fill("ក");
  const methodGroup = page.getByRole("group", { name: "Метод українського запису" });
  await expect(methodGroup.getByRole("button", { name: "Фонетичний" })).toBeVisible();
  await expect(methodGroup.getByRole("button", { name: "За романізацією" })).toBeVisible();
  await expect(page.getByRole("button", { name: "Очистити" })).toBeVisible();
});

test("romanization method can be activated by keyboard and status is announced", async ({ page }) => {
  await page.goto("/");
  await page.locator("#source").fill("Kâmpŭchéa");
  const romanizationButton = page.getByRole("button", { name: "За романізацією" });
  await romanizationButton.focus();
  await page.keyboard.press("Enter");
  await expect(romanizationButton).toHaveAttribute("aria-pressed", "true");
  await expect(page.locator("#status")).toHaveAttribute("aria-live", "polite");
  await expect(page.locator("#ua-romanization-result")).toHaveText("Кампучеа");
});
