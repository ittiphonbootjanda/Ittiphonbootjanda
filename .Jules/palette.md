## 2025-05-14 - Loading State Feedback for Video Generation
**Learning:** Providing immediate visual feedback by disabling the submit button and changing its text is critical for long-running processes like video generation. Using `setTimeout(..., 0)` in the submission handler ensures that the form's POST request is successfully initiated by the browser before the button's state change potentially interrupts it.
**Action:** Use the `setTimeout(..., 0)` pattern when disabling submit buttons to prevent form cancellation in some browser environments.

## 2025-05-14 - Accessible Focus States
**Learning:** High-contrast focus indicators, such as combining a `box-shadow` with a solid `border` or `outline` change, significantly improve keyboard navigation accessibility. This ensures that the focused element is clearly visible to users with low vision or those who rely on high-contrast modes.
**Action:** Always pair `box-shadow` focus rings with a tangible border or outline color change for interactive elements.
