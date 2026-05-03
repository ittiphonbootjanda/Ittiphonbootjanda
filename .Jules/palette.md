## 2025-05-14 - [Form Submission UX]
**Learning:** When disabling a submit button to provide loading feedback in a standard HTML form, use `setTimeout(..., 0)` to ensure the browser successfully initiates the POST request before the button state changes to disabled.
**Action:** Always wrap `submitBtn.disabled = true` in a `setTimeout` with 0 delay within the form's submit event listener.

## 2025-05-14 - [Real-time Feedback Accessibility]
**Learning:** Dynamic UI elements like character counters should use `aria-live="polite"` to ensure updates are announced to screen reader users without interrupting their current task.
**Action:** Include `aria-live="polite"` on containers for live-updating text like counters or status indicators.
