## 2026-06-23 - Accessibility Pattern for Character Counters
**Learning:** When implementing live regions for metrics like character counts, include `aria-atomic="true"` alongside `aria-live="polite"` to ensure screen readers announce the full context (e.g., '47 / 500') rather than just the updated digits.
**Action:** Always pair `aria-atomic="true"` with `aria-live` for numerical status indicators.

## 2026-06-23 - UI Feedback via Form Submission
**Learning:** Disabling a submit button immediately on click can sometimes prevent the browser from successfully initiating the form's POST request in certain environments. Using `setTimeout(..., 0)` in the submit handler allows the event loop to process the submission before the button becomes disabled.
**Action:** Use `setTimeout(() => { btn.disabled = true; }, 0)` in form submission handlers for immediate UX feedback.
