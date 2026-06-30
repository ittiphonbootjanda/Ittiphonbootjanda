## 2024-05-23 - [UX Enhancement: Feedback & Accessibility]
**Learning:** For long-running operations like video generation, providing immediate visual feedback by disabling the submit button and changing its text significantly improves the perceived responsiveness. Combining this with ARIA live regions for dynamic elements like character counters ensures the UI remains accessible to screen reader users.
**Action:** Always implement loading states for async/long-running form submissions and use `aria-live="polite"` with `aria-atomic="true"` for real-time counters.

## 2024-05-23 - [Preventing Layout Shift on Focus]
**Learning:** Adding a border on focus can cause a layout shift if not accounted for. While reducing padding is a common technique, it's often cleaner to have a transparent border on the base state with the same width as the focus border to ensure the element's dimensions remain identical.
**Action:** Use `border: 2px solid transparent` on base interactive elements if they will have a `2px solid` border on focus to prevent layout jitter.
