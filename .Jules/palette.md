## 2025-05-14 - Loading State Feedback in MPAs
**Learning:** In Multi-Page Applications (MPAs), disabling the submit button immediately on click can sometimes interfere with the form submission process in certain browsers. Using `setTimeout(fn, 0)` ensures the event loop completes the submission trigger before the button state changes.
**Action:** Always wrap submit button disabling logic in `setTimeout(..., 0)` when working with standard HTML form submissions.

## 2025-05-14 - Verifying Immediate UI State with Playwright
**Learning:** Testing immediate UI feedback (like loading states) that occurs just before a page navigation can be flaky.
**Action:** Use `page.evaluate` to add a `submit` listener that calls `e.preventDefault()` during verification to "freeze" the page in its submitting state for reliable assertions.
