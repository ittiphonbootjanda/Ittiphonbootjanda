## 2026-01-31 - [Immediate Feedback on Form Submission]
**Learning:** Disabling a submit button immediately within a 'submit' event listener can sometimes interfere with the browser's ability to include that button's value in the POST request or even stop the submission in some environments. Using `setTimeout(..., 0)` ensures the submission starts before the UI state changes.
**Action:** Use `setTimeout(..., 0)` when disabling submit buttons to provide visual feedback for long-running operations.
