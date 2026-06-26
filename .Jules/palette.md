## 2025-05-14 - Loading States and Focus Feedback

**Learning:** When adding a border for focus states, it's crucial to compensate by adjusting padding (e.g., reducing padding by the border width) to prevent layout shifts. Additionally, for form submissions that trigger long-running backend processes, providing immediate visual feedback by disabling the submit button and updating its text significantly improves perceived responsiveness.

**Action:** Always use the `border-box` sizing model and adjust padding when introducing borders on focus. Use `setTimeout(..., 0)` in form submit handlers to ensure the browser initiates the POST request before the button enters a disabled state.
