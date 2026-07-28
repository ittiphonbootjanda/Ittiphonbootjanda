## 2025-05-15 - [Improving Video Generation UX]
**Learning:** For long-running server operations (like video generation), provide immediate UI feedback to prevent multiple submissions and improve perceived performance. Using `setTimeout(..., 0)` in a form submission handler allows the browser to initiate the POST request before the button is disabled.
**Action:** Always implement a loading state for long-running form submissions by disabling the submit button and updating its text.

## 2025-05-15 - [Visual Accessibility and Focus States]
**Learning:** Standard outlines can be hard to see. A 3px semi-transparent box-shadow combined with a transparent outline provides a clear, high-contrast-friendly focus indicator that looks modern and remains accessible.
**Action:** Use `box-shadow` for focus rings with a transition for a smoother user experience.
