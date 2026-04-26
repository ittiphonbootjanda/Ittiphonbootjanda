## 2025-05-22 - Improved Feedback and Accessibility for Video Generation

**Learning:** When disabling a submit button on form submission to provide UX feedback in an MPA, using `setTimeout(..., 0)` in the JavaScript handler ensures the browser successfully initiates the POST request before the button enters the disabled state, which can otherwise cancel the request in some browsers. Also, for accessibility, dynamic UI elements like character counters should include `aria-live="polite"` to keep screen reader users informed.

**Action:** Always wrap submit button disabling logic in a `setTimeout(..., 0)` and ensure all form inputs have associated labels (visible or `visually-hidden`) and appropriate ARIA live regions for dynamic feedback.
