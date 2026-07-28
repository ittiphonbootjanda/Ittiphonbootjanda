## 2026-02-04 - [Button feedback on form submission]
**Learning:** Using `setTimeout(..., 0)` to disable a submit button ensures the browser initiates the form submission before the button becomes disabled, which is critical for UX feedback in standard form-based applications.
**Action:** Always use this pattern when disabling submit buttons to provide immediate visual feedback while ensuring form submission success.
