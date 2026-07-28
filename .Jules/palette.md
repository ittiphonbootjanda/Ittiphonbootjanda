## 2025-05-15 - [Form Submission UX]
**Learning:** When disabling a submit button to provide visual feedback (like a 'Generating...' state), using a immediate `setTimeout(..., 0)` ensures the browser successfully initiates the form's POST request before the button enters the disabled state, preventing potential submission blocks in some environments.
**Action:** Always wrap submit button disabling logic in a `setTimeout` within the `onsubmit` handler for consistent behavior.
