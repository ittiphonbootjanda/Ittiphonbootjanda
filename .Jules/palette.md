## 2025-06-09 - [Loading States in Inline Handlers]
**Learning:** In simple forms using inline `onsubmit` handlers, disabling the submit button immediately can sometimes interfere with the browser's form submission process. Using `setTimeout(..., 0)` ensures the event loop processes the submission before the button is disabled.
**Action:** Always wrap button disabling/text changes in `setTimeout(..., 0)` when implemented within an `onsubmit` attribute.
