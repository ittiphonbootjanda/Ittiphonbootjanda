## 2026-02-12 - [Loading States & Playwright Verification]
**Learning:** When using `setTimeout(..., 0)` to disable a submit button (to allow the POST request to start), standard Playwright `click()` might not capture the state before navigation.
**Action:** Use `page.evaluate` with `await new Promise(r => setTimeout(r, 0))` to capture the UI state immediately after triggering the event but before the browser processes navigation or successive JS ticks.
