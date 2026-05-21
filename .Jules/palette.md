## 2025-05-14 - [Form Accessibility and Feedback]
**Learning:** Adding a `visually-hidden` label to a textarea provides essential context for screen reader users without altering the visual design. Coupling this with `aria-live="polite"` and `aria-atomic="true"` on a character counter ensures dynamic updates are announced clearly.
**Action:** Always include a semantic `<label>` (even if visually hidden) for all form inputs and use ARIA live regions for real-time status updates like character counts.
