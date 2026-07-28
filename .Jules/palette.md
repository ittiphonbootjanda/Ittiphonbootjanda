## 2026-02-28 - Immediate Interaction Feedback
**Learning:** For long-running server-side operations (like video generation), users benefit from immediate visual feedback on the submit button to confirm the action was triggered and to prevent duplicate submissions.
**Action:** Use a JavaScript `submit` event listener to update the button's text to "Generating..." and disable it using `setTimeout(..., 0)` to ensure the browser successfully initiates the POST request before the element's state changes.

## 2026-02-28 - Accessible High-Contrast Focus States
**Learning:** Default browser focus outlines can be inconsistent or hard to see. A custom box-shadow focus state provides better visibility and design consistency.
**Action:** Use `outline: 2px solid transparent; box-shadow: 0 0 0 3px rgba(76, 175, 80, 0.4);` for focus states, ensuring they remain visible in high-contrast modes while providing a modern aesthetic.
