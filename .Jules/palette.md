## 2025-05-22 - Layout Jitter and Form Submission
**Learning:** Adjusting padding in focus states can cause layout shifts if not perfectly balanced with border-width changes. Also, disabling a submit button synchronously in an `onsubmit` handler can block the form from submitting in some browsers.
**Action:** Use consistent padding for focus states or compensate with border-box sizing. Use `setTimeout(..., 0)` to defer UI updates like disabling buttons until the browser has initiated the form submission.
