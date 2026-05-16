## 2025-05-14 - [Accessible Live Regions for Metrics]
**Learning:** When implementing live regions for real-time metrics like character counters, using `aria-live="polite"` alone may only announce the changing digits. Including `aria-atomic="true"` ensures screen readers announce the full context (e.g., "29 / 500") which is more helpful for the user.
**Action:** Always pair `aria-live="polite"` with `aria-atomic="true"` for counters and progress indicators.

## 2025-05-14 - [UX Feedback for Form Submission]
**Learning:** Disabling a submit button immediately in an `onsubmit` handler can sometimes prevent the browser from actually sending the POST request in some environments. Using `setTimeout(..., 0)` ensures the submission is initiated before the button becomes inactive.
**Action:** Use a zero-delay timeout when disabling submit buttons to provide immediate UX feedback without interfering with form lifecycle.
