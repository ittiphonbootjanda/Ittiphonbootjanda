## 2025-05-15 - [Button Loading State Implementation]
**Learning:** When disabling a submit button on form submission to provide UX feedback, use `setTimeout(..., 0)` in the JavaScript handler to ensure the browser successfully initiates the POST request before the button enters the disabled state.
**Action:** Always use this pattern for simple form submissions to avoid potential issues with form data not being sent or navigation being canceled.
