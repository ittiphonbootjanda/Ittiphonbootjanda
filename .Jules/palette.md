## 2025-05-22 - [Form feedback and accessibility]
**Learning:** When disabling a submit button on form submission to provide UX feedback in an MPA, use `setTimeout(..., 0)` in the JavaScript handler to ensure the browser successfully initiates the POST request before the button enters the disabled state. This prevents potential cancellation of the submit event.
**Action:** Always use this pattern for simple loading states in Flask or similar MPA frameworks to ensure reliable form submission.
