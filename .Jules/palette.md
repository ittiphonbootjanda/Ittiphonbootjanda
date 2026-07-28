## 2025-05-14 - Loading State Feedback in MPAs
**Learning:** In Multi-Page Applications (MPAs), disabling a submit button immediately on click can sometimes prevent the browser from initiating the form's POST request. Using `setTimeout(..., 0)` ensures the event loop completes the submission start before the UI interaction is blocked.
**Action:** Use `setTimeout(..., 0)` in form submit handlers to safely disable buttons and provide visual feedback (like "Generating...") without breaking default form behavior.

## 2025-05-14 - Accessible Focus Rings for High Contrast
**Learning:** Standard `outline: none` removes focus visibility for keyboard users, but `outline: 2px solid transparent` combined with a `box-shadow` provides a smooth, themed focus ring in standard mode while remaining visible in high-contrast modes where box-shadows might be stripped.
**Action:** Always use `outline: 2px solid transparent` when applying custom `box-shadow` focus states to ensure WCAG compliance across different rendering modes.
