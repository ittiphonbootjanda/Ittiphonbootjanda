## 2025-05-14 - Loading State with setTimeout(..., 0)
**Learning:** When disabling a submit button on form submission to provide UX feedback in an MPA, use `setTimeout(..., 0)` in the JavaScript handler to ensure the browser successfully initiates the POST request before the button enters the disabled state.
**Action:** Use `setTimeout(..., 0)` for any form submission feedback that involves disabling the trigger.

## 2025-05-14 - Focus Indicators in High Contrast
**Learning:** Using `outline: 2px solid transparent` along with `box-shadow` for focus states ensures visibility in high-contrast modes while maintaining a custom aesthetic in standard modes.
**Action:** Always include `outline: 2px solid transparent` when customizing focus states with `box-shadow`.
