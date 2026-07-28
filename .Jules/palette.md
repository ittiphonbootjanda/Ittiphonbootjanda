## 2025-05-14 - Loading State Feedback in MPAs
**Learning:** In Multi-Page Applications (MPAs) using standard form POST, disabling the submit button immediately in the 'submit' event handler can prevent the browser from actually sending the request.
**Action:** Use `setTimeout(() => { btn.disabled = true; }, 0)` in the submission handler to ensure the browser successfully initiates the POST request before the button enters the disabled state.
