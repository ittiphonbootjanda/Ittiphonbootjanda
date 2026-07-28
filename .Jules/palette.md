## 2025-05-15 - [Submit Button Feedback]
**Learning:** When disabling a submit button on form submission to provide UX feedback, use `setTimeout(..., 0)` in the JavaScript handler to ensure the browser successfully initiates the POST request before the button enters the disabled state.
**Action:** Apply this pattern for all form submissions where the button text or state changes to prevent intermittent submission failures.

## 2025-05-15 - [Keyboard Focus States]
**Learning:** To ensure visibility in high-contrast modes and provide clear feedback, use a combination of a solid border and a translucent box-shadow for focus states, while setting `outline: 2px solid transparent` to replace the default outline.
**Action:** Use `border: 2px solid #2e7d32; box-shadow: 0 0 0 3px rgba(76, 175, 80, 0.4); outline: 2px solid transparent;` as the standard focus pattern.
