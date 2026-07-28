## 2026-03-30 - Loading State Feedback in MPAs
**Learning:** In Multi-Page Applications (MPAs) where form submission triggers a full page reload, providing immediate UX feedback (like disabling a button) requires a `setTimeout(..., 0)` wrapper. This ensures the browser captures the "submit" intent and starts the request before the DOM element is modified/disabled, which could otherwise cancel the submission in some browsers.
**Action:** Always wrap button state changes (disabled, text updates) in a `setTimeout(..., 0)` during form submission handlers.

## 2026-03-30 - Verifying CSS Focus States in Playwright
**Learning:** When verifying CSS `box-shadow` or other computed properties in headless browsers, the returned values may vary slightly from the CSS source (e.g., fractional pixels due to device scale factor).
**Action:** Use partial string matches (e.g., checking for RGB components) rather than exact string equality for computed style assertions.
