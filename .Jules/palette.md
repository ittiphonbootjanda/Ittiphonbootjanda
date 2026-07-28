## 2025-05-15 - [Accessible Live Region Patterns]
**Learning:** When implementing live regions for metrics like character counts, include `aria-atomic="true"` alongside `aria-live="polite"` to ensure screen readers announce the full context (e.g., '47 / 500') rather than just the updated digits.
**Action:** Always pair `aria-live` with `aria-atomic="true"` for dynamic status indicators that require full context to be meaningful.

## 2025-05-15 - [Layout Stability during Focus]
**Learning:** Adding borders on focus can cause layout shifts if not compensated. Reducing padding by the border width maintains consistent element sizing.
**Action:** Use padding compensation (e.g., reduce padding by 1px for a 2px border replacing a 1px border) to prevent layout jitter on focus.
