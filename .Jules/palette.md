## 2025-05-21 - [Accessibility and Feedback Enhancements]
**Learning:** For forms with long-running operations like video generation, providing immediate visual feedback by disabling the submit button and updating its text significantly improves the perceived responsiveness and prevents duplicate submissions. Using `setTimeout(..., 0)` in the `onsubmit` handler ensures the browser initiates the request before the button is disabled.
**Action:** Always implement a loading state for high-latency actions and ensure character-limited inputs have real-time counters with `aria-live` attributes.
