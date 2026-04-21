## 2026-04-21 - [MPA Form Submission Feedback]
**Learning:** In Multi-Page Applications (MPA), disabling a submit button synchronously in the `submit` event handler can sometimes prevent the browser from actually sending the POST request.
**Action:** Use `setTimeout(() => { btn.disabled = true; }, 0)` to ensure the submission task is queued by the browser before the UI state changes.
