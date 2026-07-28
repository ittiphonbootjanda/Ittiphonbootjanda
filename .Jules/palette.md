## 2025-05-14 - Character Counter Accessibility with aria-atomic
**Learning:** When implementing live regions for metrics like character counts, using `aria-live="polite"` alone might cause screen readers to only announce the changed digits. Including `aria-atomic="true"` ensures the full context (e.g., "47 / 500") is announced, providing a much better experience for screen reader users.
**Action:** Always pair `aria-live` with `aria-atomic="true"` for status indicators that represent a ratio or a complete state.
