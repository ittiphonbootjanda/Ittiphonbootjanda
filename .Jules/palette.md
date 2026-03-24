## 2026-03-24 - [Micro-UX: Accessibility & Feedback]
**Learning:** For Multi-Page Applications (MPAs), using `setTimeout(..., 0)` in a form's 'submit' event listener allows the browser to initiate the POST request before the submit button is disabled. This provides immediate visual feedback without blocking the actual submission.
**Action:** Use this pattern for long-running form submissions in MPAs to prevent double-clicks and provide clear "processing" states.
