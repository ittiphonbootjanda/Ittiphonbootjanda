## 2025-05-15 - [Accessible Character Counter & Loading States]
**Learning:** For multi-step or long-running operations like video generation, immediate visual feedback (disabling button, changing text) is critical for UX, and adding accessible labels/live regions ensures the feature is usable for everyone.
**Action:** Always include `aria-live="polite"` and `aria-atomic="true"` for dynamic UI updates like character counters, and use `setTimeout(..., 0)` when disabling submit buttons to avoid blocking form submission.
