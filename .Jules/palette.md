## 2024-05-29 - Non-shifting Focus States and Form Submission Feedback

**Learning:** When adding a border for focus states (e.g., 2px instead of 1px), it's crucial to reduce the element's padding by the same amount to prevent "layout jitter" or shifts that can be jarring to users. Additionally, when disabling a submit button to provide loading feedback, using `setTimeout(..., 0)` in the `onsubmit` handler ensures the browser's form submission process is initiated before the button becomes disabled, avoiding potential race conditions where the POST request might be blocked.

**Action:** Always calculate and compensate padding when changing border widths on focus. Use the `setTimeout(..., 0)` pattern for non-destructive, immediate UX feedback on form submissions in simple applications.
