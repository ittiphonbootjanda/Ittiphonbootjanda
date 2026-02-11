## 2025-05-14 - [Focus States & High Contrast]
**Learning:** Using `outline: none` removes the default focus indicator, which is bad for accessibility if the replacement (like `box-shadow`) isn't supported or visible in all modes. Using `outline: 2px solid transparent` preserves the focus indicator for high-contrast modes while hiding it for standard users, allowing the `box-shadow` to provide a themed experience.
**Action:** Always prefer `outline: 2px solid transparent` over `outline: none` when implementing custom focus styles.

## 2025-05-14 - [Testing Async UI States]
**Learning:** Verifying UI changes triggered by `setTimeout(..., 0)` in Playwright can be flaky due to rapid navigation. Using `page.evaluate` with an internal `await new Promise(r => setTimeout(r, 0))` allows for reliable synchronous-like verification of the DOM state before the browser context is destroyed by navigation.
**Action:** Use `await page.evaluate` with a small timeout for testing transient UI states during form submissions.
