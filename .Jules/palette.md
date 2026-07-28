## 2025-05-15 - [Real-time Feedback & Accessibility]
**Learning:** Adding a character counter and a loading state significantly improves user confidence during long-running tasks like video generation. Using `aria-live="polite"` and `aria-atomic="true"` ensures these updates are accessible to screen reader users without being disruptive.
**Action:** Always include visual and programmatic feedback for asynchronous operations and text limits in future Palette tasks.
