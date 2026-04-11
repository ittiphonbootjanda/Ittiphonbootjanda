## 2025-05-22 - [Loading State & Accessibility]
**Learning:** When disabling a submit button on form submission to provide UX feedback in an MPA, use `setTimeout(..., 0)` in the JavaScript handler to ensure the browser successfully initiates the POST request before the button enters the disabled state.
**Action:** Use this pattern for form submissions where immediate feedback is needed without breaking the default form behavior.
