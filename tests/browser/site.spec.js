import { test, expect } from "@playwright/test";

test.beforeEach(async ({ page }, testInfo) => {
  if ([
    "research tools are collapsed by default and can be opened on demand",
    "IPA and Latin romanization remain visible outside the collapsed analysis drawer",
    "IPA and romanization method switches are visible beside the primary result without opening research details"
  ].includes(testInfo.title)) return;
  await page.addInitScript(() => {
    document.addEventListener("DOMContentLoaded", () => {
      const drawer = document.querySelector("#research-details");
      if (drawer) drawer.open = true;
      const settings = document.querySelector(".input-research-options");
      if (settings) settings.open = true;
    });
  });
});



test("Latin BGN/PCGN input renders a provisional Ukrainian form in the primary result", async ({ page }) => {
  await page.goto("/");
  await page.locator("#source").fill("Kampucheapcheathiptey");
  await expect(page.locator("#ua-result")).toHaveText("— · для готової романізації оберіть метод «З романізації»");
  await expect(page.locator("#status")).toContainText("IPA НЕ ЗАСТОСОВУЄТЬСЯ");
  await page.locator("#mode-romanization").click();
  await expect(page.locator("#ua-result")).toHaveText("Кампучеапчеат'іптей");
  await expect(page.locator("#status")).toContainText("РОМАНІЗАЦІЯ");
  await expect(page.locator("#ipa-result")).toContainText("IPA не застосовується");
});

test("research tools are collapsed by default and can be opened on demand", async ({ page }) => {
  await page.goto("/");
  const drawer = page.locator("#research-details");
  await page.locator("#source").fill("ក");
  await expect(page.locator("#results")).toBeVisible();
  await expect(drawer).not.toHaveAttribute("open");
  await expect(page.locator(" #ua-result")).toBeVisible();
  await drawer.locator("summary").click();
  await expect(drawer).toHaveJSProperty("open", true);
});

async function contrastRatio(page, foregroundSelector, backgroundSelector) {
  return page.evaluate(({ foregroundSelector, backgroundSelector }) => {
    const foreground = document.querySelector(foregroundSelector);
    const background = document.querySelector(backgroundSelector);
    if (!foreground || !background) return null;
    const parse = value => value.match(/[\d.]+/g).slice(0, 3).map(Number);
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

test("Khmer source-located inherent-vowel output is tier B without a DOM exception", async ({ page }) => {
  const pageErrors = [];
  page.on("pageerror", error => pageErrors.push(error.message));
  await page.goto("/");
  await page.locator("#source").fill("ក");
  await expect(page.locator("#results")).toBeVisible();
  await expect(page.locator("#ipa-result")).toHaveText("/kɑː/");
  await expect(page.locator("#ua-result")).toHaveText("ка");
  await expect(page.locator("#status")).toHaveText("PROPOSED · доказовий рівень B");
  await expect(page.locator(".unit-status")).toContainText("рівень B");
  await expect(page.locator(".unit-source-locator")).toContainText("R12A");
  expect(pageErrors).toEqual([]);
});

test("compositional Khmer phrase without a phrase-level locator remains tier C", async ({ page }) => {
  await page.goto("/");
  await page.locator("#source").fill("ភាសាខ្មែរ");
  await expect(page.locator("#results")).toBeVisible();
  await expect(page.locator("#status")).toHaveText("PROPOSED · доказовий рівень C");
});


test("Wiktionary lexical fixtures expose exact source locators at tier B", async ({ page }) => {
  for (const source of ["ខ្មែរ", "ភាសា", "ភ្នំពេញ", "កម្ពុជា", "ខ្ញុំ", "ជាខ្មែរ", "ល្ងាច", "អក្សរខ្មែរ", "នគរខ្មែរ", "អក្សរមូល"]) {
    await page.goto("/");
    await page.locator("#source").fill(source);
    await expect(page.locator("#status")).toHaveText("PROPOSED · доказовий рівень B");
    await expect(page.locator(".unit-source-locator")).toContainText("Wiktionary");
  }
});

test("directly source-attested Khmer phrase is tier B and differs from composition-only phrase", async ({ page }) => {
  await page.goto("/");
  await page.locator("#source").fill("ជាខ្មែរ");
  await expect(page.locator("#ipa-result")).toHaveText("/ciə ˈkʰmae/");
  await expect(page.locator("#ua-result")).toHaveText("тьіє к'мае");
  await expect(page.locator("#status")).toHaveText("PROPOSED · доказовий рівень B");
  await expect(page.locator(".unit-source-locator")).toContainText("Wiktionary");
  await expect(page.locator(".unit-source-locator")).toContainText("oldid=68806374");
});

test("IPA and Latin romanization remain visible outside the collapsed analysis drawer", async ({ page }) => {
  await page.goto("/");
  await page.getByRole("textbox").fill("សុខា");
  await expect(page.locator("#ipa-result")).toBeVisible();
  await expect(page.locator("#romanization-result")).toBeVisible();
  await expect(page.locator("#research-details")).not.toHaveAttribute("open", "");
  await expect(page.locator("#unit-details")).toBeHidden();
});

test("source-attested Khmer cluster word retains every IPA segment through the adapter", async ({ page }) => {
  await page.goto("/");
  await page.locator("#source").fill("ល្ងាច");
  await expect(page.locator("#ipa-result")).toHaveText("/lŋiəc/");
  await expect(page.locator("#ua-result")).toHaveText("лнгієть");
  await expect(page.locator("#status")).toHaveText("PROPOSED · доказовий рівень B");
  await expect(page.locator(".unit-source-locator")).toContainText("oldid=68625783");
});

test("long-vowel lexical IPA is preserved while the Ukrainian adapter omits quantity", async ({ page }) => {
  const cases = [
    ["អក្សរខ្មែរ", "/ʔak.ˈsɑː kʰmae/", "акса к'мае", "87132823"],
    ["នគរខ្មែរ", "/nɔ.ˈkɔː kʰmae/", "ноко к'мае", "84887163"],
    ["អក្សរមូល", "/ʔak.ˈsɑː muːl/", "акса мул", "63698235"],
  ];
  for (const [source, ipa, ukrainian, oldid] of cases) {
    await page.goto("/");
    await page.locator("#source").fill(source);
    await expect(page.locator("#ipa-result")).toHaveText(ipa);
    await expect(page.locator("#ua-result")).toHaveText(ukrainian);
    await expect(page.locator("#status")).toHaveText("PROPOSED · доказовий рівень B");
    await expect(page.locator(".unit-source-locator")).toContainText("oldid=" + oldid);
  }
});

test("unsupported grapheme is marked locally", async ({ page }) => {
  await page.goto("/");
  await page.locator("#source").fill("កx");
  await expect(page.locator("#results")).toBeVisible();
  await expect(page.locator("#status")).toHaveText("EVIDENCE LIMITED · доказовий рівень D");
  await expect(page.locator("#ipa-result")).toHaveText("/kɑː/⟦INVALID_OR_UNSUPPORTED⟧");
  await expect(page.locator("#ua-result")).toHaveText("ка???");
});

test("mixed scripts and Khmer numerals preserve neighboring output and source order", async ({ page }) => {
  await page.goto("/");
  await page.locator("#source").fill("កLlenguatgeគ៦១១");
  await expect(page.locator("#results")).toBeVisible();
  await expect(page.locator("#status")).toHaveText("EVIDENCE LIMITED · доказовий рівень D");
  await expect(page.locator("#ipa-result")).toHaveText("/kɑː/⟦INVALID_OR_UNSUPPORTED⟧/kɔː/៦១១");
  await expect(page.locator("#ua-result")).toHaveText("како???៦១១");
});

test("one unsupported unit does not hide neighboring IPA and Ukrainian output", async ({ page }) => {
  await page.goto("/");
  await page.locator("#source").fill("ក ☃ គ");
  await expect(page.locator("#results")).toBeVisible();
  await expect(page.locator("#status")).toHaveText("EVIDENCE LIMITED · доказовий рівень D");
  await expect(page.locator("#ipa-result")).toHaveText("/kɑː/ ⟦INVALID_OR_UNSUPPORTED⟧ /kɔː/");
  await expect(page.locator("#ua-result")).toHaveText("ка ??? ко");
});

test("clear control restores the empty state", async ({ page }) => {
  await page.goto("/");
  await page.locator("#source").fill("ក");
  await page.locator("#clear").click();
  await expect(page.locator("#results")).toBeHidden();
  await expect(page.locator("#empty")).toBeVisible();
});


test("IPA and romanization method switches are visible beside the primary result without opening research details", async ({ page }) => {
  await page.goto("/");
  await page.locator("#source").fill("Kâmpŭchéa");
  const drawer = page.locator("#research-details");
  await expect(drawer).not.toHaveAttribute("open", "");
  const group = page.getByRole("group", { name: "Метод українського запису" });
  await expect(group).toBeVisible();
  await expect(group.getByRole("button", { name: "За IPA" })).toBeVisible();
  await expect(group.getByRole("button", { name: "З романізації" })).toBeVisible();
  await expect(page.locator("#ua-result-title")).toHaveText("Українська за вимовою (IPA)");
  await expect(page.locator("#ua-result")).toContainText("IPA не застосовується");
  await group.getByRole("button", { name: "З романізації" }).click();
  await expect(page.locator("#ua-result-title")).toHaveText("Українська з романізації");
  await expect(page.locator("#ua-result")).toHaveText("Кампучеа");
  await group.getByRole("button", { name: "За IPA" }).click();
  await expect(page.locator("#ua-result-title")).toHaveText("Українська за вимовою (IPA)");
  await expect(page.locator("#ua-result")).toContainText("IPA не застосовується");
});

test("romanization mode renders a separate provisional Ukrainian form", async ({ page }) => {
  await page.goto("/");
  await page.locator("#source").fill("សុខា");
  await page.locator("#mode-romanization").click();
  await expect(page.locator("#romanization-result")).toHaveText("Sokha");
  await expect(page.locator("#ua-romanization-result")).toHaveText("Сок'а");
  await expect(page.locator("#ua-result")).toHaveText("Сок'а");
  await expect(page.locator("#ua-romanization-status")).toContainText("PROVISIONAL");
  await expect(page.locator("#ipa-result")).toBeVisible();
});


test("pre-romanized BGN/PCGN input maps directly to Ukrainian with diacritics", async ({ page }) => {
  await page.goto("/");
  await page.locator("#source").fill("Kâmpŭchéa");
  await page.locator("#mode-romanization").click();
  await expect(page.locator("#romanization-result")).toHaveText("Kâmpŭchéa");
  await expect(page.locator("#ua-romanization-result")).toHaveText("Кампучеа");
  await expect(page.locator("#ua-result")).toHaveText("Кампучеа");
  await expect(page.locator("#ua-romanization-status")).toContainText("PROVISIONAL");
  await expect(page.locator("#romanization-title")).toHaveText("Вхідна романізація · BGN/PCGN 1972");
  await expect(page.locator("#ipa-result")).toBeVisible();
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
  await expect(methodGroup.getByRole("button", { name: "За IPA" })).toBeVisible();
  await expect(methodGroup.getByRole("button", { name: "З романізації" })).toBeVisible();
  await expect(page.getByRole("button", { name: "Очистити" })).toBeVisible();
});

test("romanization method can be activated by keyboard and status is announced", async ({ page }) => {
  await page.goto("/");
  await page.locator("#source").fill("Kâmpŭchéa");
  const romanizationButton = page.getByRole("button", { name: "З романізації" });
  await romanizationButton.focus();
  await page.keyboard.press("Enter");
  await expect(romanizationButton).toHaveAttribute("aria-pressed", "true");
  await expect(page.locator("#status")).toHaveAttribute("aria-live", "polite");
  await expect(page.locator("#ua-romanization-result")).toHaveText("Кампучеа");
});



test("unresolved Khmer phrase offers per-unit Ukrainian candidates while keeping IPA unresolved", async ({ page }) => {
  await page.goto("/");
  await page.locator("#source").fill("កម្ពុជាប្រជាធិបតេយ្យ");
  await expect(page.locator("#ipa-result")).toHaveText("⟦NOT_ESTABLISHED⟧");
  await expect(page.locator("#ua-result")).toHaveText("Кампучеапчеат'іптей");
  await expect(page.locator("#ua-result")).not.toContainText("???");
  await expect(page.locator("#status")).toContainText("PROVISIONAL CANDIDATE");
  await expect(page.locator("#unit-details")).toContainText("Попередня українська форма:");
  await expect(page.locator("#unit-details")).toContainText("BGN/PCGN, не IPA");
});

test("best-effort Ukrainian candidates are automatic at every detail level", async ({ page }) => {
  await page.goto("/");
  await page.locator("#source").fill("កម្ពុជាប្រជាធិបតេយ្យ");
  for (const level of ["strict", "balanced", "exploratory"]) {
    await page.locator("#output-level").selectOption(level);
    await expect(page.locator("#ua-result")).toHaveText("Кампучеапчеат'іптей");
    await expect(page.locator("#ipa-result")).toHaveText("⟦NOT_ESTABLISHED⟧");
  }
});

test("unresolved Khmer cluster offers a romanization candidate instead of only an onset hint", async ({ page }) => {
  await page.goto("/");
  await page.locator("#source").fill("ក្ក");
  await expect(page.locator("#ipa-result")).toHaveText("⟦NOT_ESTABLISHED⟧");
  await expect(page.locator("#ua-result")).not.toContainText("???");
  await expect(page.locator("#status")).toContainText("PROVISIONAL CANDIDATE");
  await expect(page.locator("#unit-details")).toContainText("Попередня українська форма:");
  await expect(page.locator(".unit-detail")).toHaveAttribute("data-fallback-rule-id", "KHMER-BGN-PCGN-ORTHOGRAPHIC-FALLBACK-V1");
  await expect(page.locator(".unit-detail")).toHaveAttribute("data-fallback-position", "whole-unit");
});


test("service page keeps visible controls usable by keyboard after results appear", async ({ page }) => {
  await page.goto("/");
  await page.locator("#source").fill("ក");
  const example = page.getByRole("button", { name: /Приклад/ });
  await example.focus();
  await expect(example).toBeFocused();
  const outline = await example.evaluate(element => {
    const style = getComputedStyle(element);
    return { width: style.outlineWidth, style: style.outlineStyle };
  });
  expect(outline.width).not.toBe("0px");
  expect(outline.style).not.toBe("none");

  const clear = page.getByRole("button", { name: "Очистити" });
  await clear.focus();
  await page.keyboard.press("Space");
  await expect(page.locator("#results")).toBeHidden();
  await expect(page.locator("#empty")).toBeVisible();
});

test("service and methodology pages do not create document-level horizontal overflow on narrow screens", async ({ page }) => {
  for (const path of ["/", "/system.html"]) {
    for (const width of [320, 375, 420]) {
      await page.setViewportSize({ width, height: 900 });
      await page.goto(path);
      const dimensions = await page.evaluate(() => ({
        viewport: document.documentElement.clientWidth,
        document: document.documentElement.scrollWidth,
        body: document.body.scrollWidth,
      }));
      expect(dimensions.document, `${path} at ${width}px: ${JSON.stringify(dimensions)}`).toBeLessThanOrEqual(dimensions.viewport);
      expect(dimensions.body, `${path} at ${width}px: ${JSON.stringify(dimensions)}`).toBeLessThanOrEqual(dimensions.viewport);
    }
  }
});


test("service and methodology pages expose coherent document landmarks and named controls", async ({ page }) => {
  for (const path of ["/", "/system.html"]) {
    await page.goto(path);
    const structure = await page.evaluate(() => {
      const accessibleName = element => {
        const labelledBy = element.getAttribute("aria-labelledby");
        const referenced = labelledBy
          ? labelledBy.split(/\s+/).map(id => document.getElementById(id)?.textContent ?? "").join(" ")
          : "";
        const labels = element.labels
          ? Array.from(element.labels).map(label => label.textContent ?? "").join(" ")
          : "";
        return (
          element.getAttribute("aria-label") ||
          referenced ||
          labels ||
          element.innerText ||
          element.textContent ||
          element.getAttribute("title") ||
          ""
        ).replace(/\s+/g, " ").trim();
      };
      const controls = Array.from(document.querySelectorAll("button, input, select, textarea"));
      const links = Array.from(document.querySelectorAll("a[href]"));
      return {
        language: document.documentElement.lang,
        mainLandmarks: document.querySelectorAll("main, [role='main']").length,
        h1Count: document.querySelectorAll("h1").length,
        unnamedControls: controls.filter(element => !accessibleName(element)).map(element => element.outerHTML.slice(0, 180)),
        unnamedLinks: links.filter(element => !accessibleName(element)).map(element => element.outerHTML.slice(0, 180)),
        imagesWithoutAlt: Array.from(document.images).filter(image => !image.hasAttribute("alt")).map(image => image.outerHTML.slice(0, 180)),
      };
    });
    expect(structure.language, path).toBe("uk");
    expect(structure.mainLandmarks, path).toBe(1);
    expect(structure.h1Count, path).toBe(1);
    expect(structure.unnamedControls, path).toEqual([]);
    expect(structure.unnamedLinks, path).toEqual([]);
    expect(structure.imagesWithoutAlt, path).toEqual([]);
  }

  await page.goto("/");
  await expect(page.getByRole("navigation", { name: "Основна навігація" })).toBeVisible();
  await expect(page.getByRole("main")).toBeVisible();
  await expect(page.getByRole("textbox", { name: "Введіть кмерський текст або латинську романізацію BGN/PCGN 1972" })).toBeVisible();
});
