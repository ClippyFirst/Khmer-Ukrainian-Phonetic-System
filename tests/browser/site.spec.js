import { test, expect } from "@playwright/test";

async function contrastRatio(page, foregroundSelector, backgroundSelector) {
  return page.evaluate(({ foregroundSelector, backgroundSelector }) => {
    const foreground = document.querySelector(foregroundSelector);
    const background = document.querySelector(backgroundSelector);
    if (!foreground || !background) return null;
    const parse = value => value.match(/[\\d.]+/g).slice(0, 3).map(Number);
    const luminance = value => {
      const [r, g, b] = parse(value).map(channel => {
        const normalized = channel / 255;
        return normalized <= 0.04045 ? normalized / 12.92 : ((normalized + 0.055) / 1.055) ** 2.4;
      });
      return 0.2126 * r + 0.7152 * g + 0.0722 * b;
    };
    const fg = luminance(getComputedStyle(foreground).color);
    const bg = luminance(getComputedStyle(background).backgroundColor);
    return (Math.max(fg, bg) + 0.05) / (Math.min(fg, bg) + 0.05);
  }, { foregroundSelector, backgroundSelector });
}

test("key service-page text styles meet WCAG AA normal-text contrast", async ({ page }) => {
  await page.goto("/");
  await page.locator("#source").fill("ក");
  await page.keyboard.press("Tab");
  const pairs = [
    [".eyebrow", "body"],
    [".hint", "textarea"],
    [".num", ".workspace"],
    [".meta > span", ".result-card"],
    [".button.primary", ".button.primary"],
    [".skip-link", ".skip-link"]
  ];
  for (const [foreground, background] of pairs) {
    const ratio = await contrastRatio(page, foreground, background);
    expect(ratio, `${foreground} against ${background}`).not.toBeNull();
    expect(ratio, `${foreground} against ${background}: ${ratio}`).toBeGreaterThanOrEqual(4.5);
  }
});

test("key methodology-page text styles meet WCAG AA normal-text contrast", async ({ page }) => {
  await page.goto("/system.html");
  await page.keyboard.press("Tab");
  const pairs = [
    [".doc .muted", "body"],
    [".docno", "body"],
    [".skip-link", ".skip-link"]
  ];
  for (const [foreground, background] of pairs) {
    const ratio = await contrastRatio(page, foreground, background);
    expect(ratio, `${foreground} against ${background}`).not.toBeNull();
    expect(ratio, `${foreground} against ${background}: ${ratio}`).toBeGreaterThanOrEqual(4.5);
  }
});


test("service page exposes a keyboard skip link to the main content", async ({ page }) => {
  await page.goto("/");
  const skipLink = page.getByRole("link", { name: "Перейти до основного вмісту" });
  await page.keyboard.press("Tab");
  await expect(skipLink).toBeFocused();
  await expect(skipLink).toBeVisible();
  await page.keyboard.press("Enter");
  await expect(page).toHaveURL(/#main-content$/);
  await expect(page.locator("#main-content")).toBeFocused();
});

test("methodology page exposes the same keyboard skip navigation", async ({ page }) => {
  await page.goto("/system.html");
  const skipLink = page.getByRole("link", { name: "Перейти до основного вмісту" });
  await page.keyboard.press("Tab");
  await expect(skipLink).toBeFocused();
  await expect(skipLink).toBeVisible();
  await page.keyboard.press("Enter");
  await expect(page).toHaveURL(/#main-content$/);
  await expect(page.locator("#main-content")).toBeFocused();
});

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

test("unsupported grapheme is marked locally", async ({ page }) => {
  await page.goto("/");
  await page.locator("#source").fill("កx");
  await expect(page.locator("#results")).toBeVisible();
  await expect(page.locator("#status")).toHaveText("EVIDENCE LIMITED");
  await expect(page.locator("#ipa-result")).toHaveText("/kɑː/⟦INVALID_OR_UNSUPPORTED⟧");
  await expect(page.locator("#ua-result")).toHaveText("ка⟦НЕПІДТРИМУЄТЬСЯ⟧");
});

test("mixed scripts and Khmer numerals preserve neighboring output and source order", async ({ page }) => {
  await page.goto("/");
  await page.locator("#source").fill("កLlenguatgeគ៦១១");
  await expect(page.locator("#results")).toBeVisible();
  await expect(page.locator("#status")).toHaveText("EVIDENCE LIMITED");
  await expect(page.locator("#ipa-result")).toHaveText("/kɑː/⟦INVALID_OR_UNSUPPORTED⟧/kɔː/៦១១");
  await expect(page.locator("#ua-result")).toHaveText("ка⟦НЕПІДТРИМУЄТЬСЯ⟧ко៦១១");
});

test("one unsupported unit does not hide neighboring IPA and Ukrainian output", async ({ page }) => {
  await page.goto("/");
  await page.locator("#source").fill("ក ☃ គ");
  await expect(page.locator("#results")).toBeVisible();
  await expect(page.locator("#status")).toHaveText("EVIDENCE LIMITED");
  await expect(page.locator("#ipa-result")).toHaveText("/kɑː/ ⟦INVALID_OR_UNSUPPORTED⟧ /kɔː/");
  await expect(page.locator("#ua-result")).toHaveText("ка ⟦НЕПІДТРИМУЄТЬСЯ⟧ ко");
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


test("shared onset fallback fixture keeps canonical output unresolved", async ({ page }) => {
  const { readFileSync } = await import("node:fs");
  const fixture = JSON.parse(readFileSync(new URL("../../data/tests/khmer-onset-fallback-fixtures.json", import.meta.url), "utf8"));
  expect(fixture.schema).toBe("khmer-onset-fallback-fixtures/v1");

  await page.goto("/");
  for (const item of fixture.cases) {
    await page.locator("#source").fill(item.source);
    await expect(page.locator("#results")).toBeVisible();
    await expect(page.locator("#ipa-result")).toHaveText(item.canonical_ipa_display);
    await expect(page.locator("#ua-result")).toHaveText(item.canonical_ukrainian_display);
    await expect(page.locator("#status")).toHaveText("NOT ESTABLISHED");
    await expect(page.locator("#unit-details")).toContainText("Попередня підказка: " + item.provisional_ipa + " → " + item.provisional_ukrainian + " [PROVISIONAL]");
    await expect(page.locator(".unit-detail")).toHaveAttribute("data-fallback-rule-id", item.rule_id);
    await expect(page.locator(".unit-detail")).toHaveAttribute("data-fallback-position", item.position);
  }
});
