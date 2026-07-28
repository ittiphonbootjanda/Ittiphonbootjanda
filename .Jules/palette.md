## 2025-05-15 - [Layout Shift Prevention]
**Learning:** When increasing border-width on focus (e.g., from 1px to 2px), compensate by reducing padding by an equal amount (e.g., from 10px to 9px). This prevents the element from "jumping" and maintains visual stability.
**Action:** Always verify focus state transitions for layout shifts and use padding compensation when applying thicker borders on focus.

## 2025-05-15 - [Accessible Live Regions for Counters]
**Learning:** Character counters benefit from `aria-live="polite"` and `aria-atomic="true"`. This ensures screen readers announce the full updated state (e.g., "11 / 500") rather than just the changed digits, providing better context.
**Action:** Use `aria-live="polite"` and `aria-atomic="true"` for dynamic character counters.
