## 2026-05-20 - [UX Enhancement: Loading States]
**Learning:** For long-running operations like video generation, providing immediate visual feedback by disabling the submit button and updating its label (e.g., "Generating...") significantly reduces user uncertainty and prevents multiple submissions. Compact inline JavaScript can achieve this effectively within strict line-count limits.
**Action:** Always implement a loading state for form submissions that trigger background processing, ensuring the button is visually distinct and conveys the current status.
