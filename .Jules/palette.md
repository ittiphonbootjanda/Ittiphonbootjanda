## 2026-05-11 - [Form Interactivity and Accessibility Polish]
**Learning:** Real-time feedback like character counters should use `aria-live="polite"` to be accessible to screen reader users without being intrusive. When increasing border width on focus (e.g., from 1px to 2px), compensate by decreasing padding by the same amount to prevent "jank" or layout shifts.
**Action:** Always use `aria-live` for dynamic text updates and use padding compensation for focus states that change border thickness.

**Learning:** Browsers may fail to submit a form if the submit button is disabled immediately in the `submit` event handler.
**Action:** Use `setTimeout(() => { btn.disabled = true; }, 0)` to allow the browser to register the submission before the button becomes inactive.

**Learning:** The CSS cursor property for a "disabled" state is `not-allowed`, not `not_allowed`.
**Action:** Use a hyphen for `not-allowed`.
