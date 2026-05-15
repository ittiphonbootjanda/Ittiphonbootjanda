## 2025-05-15 - [Layout-stable focus states]
**Learning:** When increasing border width on focus, decrease padding by the same amount to prevent layout shifts.
**Action:** Use `padding: 10px; border: 1px solid #ccc;` for normal state and `padding: 9px; border: 2px solid #2e7d32;` for focus state.

## 2025-05-15 - [Accessible live regions for counters]
**Learning:** Use `aria-live="polite"` and `aria-atomic="true"` for character counters to ensure screen readers announce the full context (e.g., "47 / 500").
**Action:** Add `aria-live="polite" aria-atomic="true"` to dynamic counter elements.
