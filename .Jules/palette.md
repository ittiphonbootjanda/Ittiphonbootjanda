## 2025-05-15 - Loading State and Focus Feedback
**Learning:** For long-running processes like video generation, providing immediate visual feedback by disabling the submit button and changing its text is critical for a good UX. Additionally, ensuring focus states do not cause layout shifts maintains visual stability.
**Action:** Always implement `onsubmit` handlers for forms that trigger long-running backend tasks and use padding compensation for border-based focus states.
