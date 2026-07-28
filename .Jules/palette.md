## 2025-04-05 - [MPA Loading State Feedback]
**Learning:** When disabling a submit button on form submission to provide UX feedback in a Multi-Page Application (MPA), using `setTimeout(..., 0)` in the JavaScript handler ensures the browser successfully initiates the POST request before the button enters the disabled state, preventing the request from being cancelled.
**Action:** Always wrap `btn.disabled = true` in a `setTimeout(..., 0)` when handling form `submit` events for immediate UI feedback.

## 2025-04-05 - [Accessible Focus States]
**Learning:** High-contrast focus states (e.g., 3px box-shadow with a 2px solid border) combined with `outline: 2px solid transparent` ensures visibility for both standard and high-contrast mode users while providing a modern, polished look.
**Action:** Use the `box-shadow` and `border` pattern for focus states on all interactive elements.
