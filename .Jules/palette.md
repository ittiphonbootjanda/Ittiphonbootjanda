## 2026-03-22 - [Loading States in MPAs]
**Learning:** When disabling a submit button on form submission in a Multi-Page Application (MPA) to provide UX feedback, using `setTimeout(..., 0)` in the JavaScript handler ensures the browser successfully initiates the POST request before the button enters the disabled state.
**Action:** Use `setTimeout(..., 0)` for immediate UI feedback on form submissions that lead to page navigation.

## 2026-03-22 - [Testing Immediate UI State on Submission]
**Learning:** To verify UI state changes (like button disabling) triggered by form submission in an MPA using Playwright, injecting a `submit` event listener that calls `e.preventDefault()` allows capturing the state before the browser navigates away.
**Action:** Use `page.evaluate` to add `preventDefault` on form submission when testing transient UI states in MPAs.
