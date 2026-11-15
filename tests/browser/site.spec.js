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
