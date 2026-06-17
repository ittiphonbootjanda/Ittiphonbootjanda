## 2025-05-15 - Layout-Preserving Focus States
**Learning:** When adding a border to an element on focus (e.g., changing from 1px to 2px), it causes a layout shift (jitter) if the total dimensions are not compensated.
**Action:** Use a negative adjustment on padding equal to the increase in border width to maintain consistent element sizing during state transitions.

## 2025-05-15 - Accessible Live Regions for Counters
**Learning:** For character counters to be meaningful to screen reader users, they need `aria-live="polite"` to announce updates without interrupting, and `aria-atomic="true"` to ensure the full context (e.g., "26 / 500") is read rather than just the changing digit.
**Action:** Always pair `aria-live` with `aria-atomic` for fractional or contextual counters.
