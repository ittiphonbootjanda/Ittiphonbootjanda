## 2025-05-15 - Accessible Character Counters
**Learning:** For dynamic character counters, using `aria-live="polite"` with `aria-atomic="true"` ensures screen readers announce the full updated state (e.g., "11 / 500") rather than just the changed digits, providing better context.
**Action:** Always include `aria-atomic="true"` when implementing real-time metrics for screen reader users.
