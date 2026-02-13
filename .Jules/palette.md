## 2025-02-13 - Reliable Loading Feedback for Forms
**Learning:** When disabling a submit button on form submission to provide UX feedback, use `setTimeout(..., 0)` to ensure the browser successfully initiates the POST request before the button enters the disabled state.
**Action:** Always wrap button disabling/text changes in a `setTimeout` when handling native form submissions.

## 2025-02-13 - Accessible Focus Indicators
**Learning:** Focus states for interactive elements should use a visible indicator like a `box-shadow` instead of `outline: none` to support keyboard navigation and high-contrast modes.
**Action:** Use a 3px green box-shadow (rgba(76, 175, 80, 0.4)) with `outline: 2px solid transparent` for focus states.

## 2025-02-13 - Screen-Reader-Only Labels
**Learning:** Interactive elements without visible text (like those relying on placeholders) need associated `<label>` elements. A `.visually-hidden` CSS class can provide these labels to screen readers without affecting the visual layout.
**Action:** Implement a standard `.visually-hidden` class and use it for all non-visible form labels.
