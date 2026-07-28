## 2026-05-07 - [Submit Button Loading State Pattern]
**Learning:** When disabling a submit button on form submission to provide UX feedback, use setTimeout(..., 0) in the JavaScript handler to ensure the browser successfully initiates the POST request before the button enters the disabled state.
**Action:** Always wrap `btn.disabled = true` in a `setTimeout` when triggered by a form's `submit` event.

## 2026-05-07 - [Accessible Focus States]
**Learning:** Focus states for interactive elements (textarea, buttons) should use a combination of `box-shadow` and `border` with `outline: 2px solid transparent` to ensure visibility across different browsers and high-contrast modes.
**Action:** Use `box-shadow: 0 0 0 3px rgba(76, 175, 80, 0.4)` and a solid border for focus states.
