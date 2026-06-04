## 2025-05-15 - [Enhancing Long-Running Form Feedback]
**Learning:** For long-running operations like video generation, providing immediate visual feedback by disabling the submit button and changing its text (e.g., "Generating...") significantly improves the perceived responsiveness of the application and prevents duplicate submissions. Using `setTimeout(..., 0)` in the `onsubmit` handler ensures the browser's form submission process starts before the button is disabled.

**Action:** Always implement a loading state for long-running form submissions. Use a combination of `aria-live` for dynamic status updates (like character counters) and button state changes to ensure a smooth and accessible user experience.
