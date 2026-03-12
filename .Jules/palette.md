## 2025-05-15 - Multi-Page Application (MPA) Loading State Feedback
**Learning:** In an MPA where form submission triggers a full page reload, providing immediate visual feedback (like disabling the button and changing its text) requires a careful balance. Using `setTimeout(..., 0)` in the submit event handler ensures that the browser initiates the POST request before the button is disabled, which could otherwise interfere with the submission in some browsers or edge cases.
**Action:** Use `setTimeout(..., 0)` for submit button state changes in MPAs to provide UX feedback without blocking form submission.

## 2025-05-15 - Visual Accessibility and Focus States
**Learning:** Standard focus outlines can be visually jarring or inconsistent across browsers. Implementing a custom focus state using a subtle border-color change and a semi-transparent box-shadow, paired with a short transition, maintains accessibility for keyboard users while providing a more polished and modern feel.
**Action:** Always pair custom focus styles with `transition` for a smoother user experience and ensure high-contrast mode compatibility by setting `outline: 2px solid transparent`.
