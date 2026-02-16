## 2026-02-16 - Loading state on long-running form submissions
**Learning:** When a form submission triggers a long-running process (like video generation), providing immediate visual feedback is crucial. However, disabling the submit button immediately can sometimes prevent the form from submitting in certain browsers. Using `setTimeout(..., 0)` ensures the submission process has started before the UI is updated to a disabled state.
**Action:** Always use `setTimeout(..., 0)` when disabling submit buttons upon form submission.
