## 2026-06-06 - [Text to Video Generator UX Improvements]
**Learning:** For long-running server-side processes like video generation, providing immediate visual feedback (disabling button, changing text to "Generating...") prevents multiple submissions and improves perceived performance. Using a character counter for limited inputs helps users stay within bounds before submission.
**Action:** Always implement loading states for form submissions that trigger heavy background tasks, and use visually hidden labels to maintain accessibility without altering the visual design intent.
