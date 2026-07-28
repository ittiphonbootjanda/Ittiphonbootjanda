## 2025-05-15 - [Character Counter & Loading States]
**Learning:** Real-time feedback like character counters should use `aria-live="polite"` and `aria-atomic="true"` to ensure screen readers announce the full context (e.g., '11 / 500') rather than just the change. Slow operations like video generation MUST have immediate visual feedback (e.g., disabling the button and changing its text) to prevent double-submissions and user confusion.
**Action:** Always include live regions for dynamic metrics and provide clear loading states for any process taking more than a few hundred milliseconds.
