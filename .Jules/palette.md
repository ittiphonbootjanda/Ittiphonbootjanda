## 2026-07-03 - [Live Regions for Character Counters]
**Learning:** When implementing live regions for metrics like character counts, include `aria-atomic="true"` alongside `aria-live="polite"` to ensure screen readers announce the full context (e.g., '47 / 500') rather than just the updated digits.
**Action:** Always pair `aria-atomic="true"` with `aria-live` for counters and status indicators.

## 2026-07-03 - [Preventing Layout Shift on Focus]
**Learning:** Adding a border on focus can cause layout jitter if the base element doesn't have a border of the same width.
**Action:** Use a transparent border of the same width in the base state, or adjust padding/margin to compensate for the border width on focus. In this case, I used `border: 2px solid transparent; border-color: #ccc;` to ensure the 2px width is always present.
