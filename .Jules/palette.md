## 2026-04-18 - [Pattern] Feedback on Long-running Form Submissions
**Learning:** For multi-page applications, providing immediate UI feedback (like disabling the submit button and changing its text) during form submission helps prevent double-submits and informs the user that the process has started. Using `setTimeout(..., 0)` in the submission handler ensures the browser's form submission logic is triggered before the element is disabled.
**Action:** Use the `setTimeout(..., 0)` pattern when disabling submit buttons on form submission to maintain native behavior while improving UX.
