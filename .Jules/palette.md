## 2026-02-24 - MPA Loading Feedback Pattern
**Learning:** In Multi-Page Applications (MPA), immediately disabling a submit button on form submission can sometimes prevent the browser from initiating the POST request. Using `setTimeout(..., 0)` ensures the event loop completes the request initiation before the UI state changes.
**Action:** Use `setTimeout(callback, 0)` for submit button feedback in MPA forms.

## 2026-02-24 - Playwright Visibility for Accessible Hidden Elements
**Learning:** Elements styled with `.visually-hidden` often retain dimensions for screen reader compatibility, causing Playwright's `expect().to_be_hidden()` to fail.
**Action:** Verify `.visually-hidden` elements by checking their class name and CSS properties (like `clip` or `rect` dimensions) rather than using standard visibility assertions.
