## 2026-03-31 - Focus States and Submission Feedback
**Learning:** For clean, card-based layouts, using a subtle `box-shadow` focus ring (e.g., `rgba(76, 175, 80, 0.4)`) provides better visual harmony than default browser outlines while maintaining accessibility. When disabling submit buttons for feedback, `setTimeout(..., 0)` is essential to ensure the form POST is dispatched before the DOM element is disabled.
**Action:** Always use `box-shadow` for focus rings and `setTimeout` for button-disabling feedback in similar MPA (Multi-Page Application) contexts.
