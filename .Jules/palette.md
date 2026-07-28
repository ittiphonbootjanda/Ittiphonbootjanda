## 2025-05-14 - [Accessible Character Counter and Smooth Focus States]
**Learning:** For real-time metrics like character counts, using `aria-live="polite"` with `aria-atomic="true"` ensures screen readers announce the full context (e.g., '47 / 500') instead of just the change. Additionally, preventing layout shifts during focus transitions can be achieved by offsetting border increases with equivalent padding decreases.
**Action:** Always combine `aria-atomic="true"` with live regions for counter-like elements, and use "padding-compensation" when adding borders on focus.
