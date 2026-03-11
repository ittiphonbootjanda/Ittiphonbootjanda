## 2026-03-11 - Accessibility labels and loading states
**Learning:** For multi-page applications with long-running server tasks (like video generation), providing immediate UI feedback by disabling the submit button and updating its text via JavaScript is crucial to prevent multiple submissions and improve perceived performance. Using a `.visually-hidden` class for form labels ensures accessibility for screen readers without altering the visual design.
**Action:** Always include a loading state for form submissions and use `.visually-hidden` labels for otherwise unlabeled inputs.
