## 2025-03-03 - [MPA Loading State Feedback]
**Learning:** For Multi-Page Applications (MPA) using standard form submissions, providing immediate UI feedback (like disabling a button) requires careful timing. Using `setTimeout(..., 0)` ensures the browser registers the form submission before the button is disabled, which might otherwise cancel the request in some browsers.
**Action:** Always use `setTimeout` when disabling a submit button in an MPA context to ensure the POST request is initiated.
