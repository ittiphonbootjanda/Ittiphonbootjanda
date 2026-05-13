## 2025-05-15 - [Accessible Live Regions for Metrics]
**Learning:** When implementing live regions for metrics like character counts (e.g., '47 / 500'), including `aria-atomic="true"` ensures screen readers announce the full context of the update rather than just the changed digits, providing better clarity for the user.
**Action:** Always pair `aria-live="polite"` with `aria-atomic="true"` for dynamic UI elements that display state as a ratio or composite string.
