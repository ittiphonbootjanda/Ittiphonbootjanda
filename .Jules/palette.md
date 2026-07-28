## 2026-02-23 - Focus States and Loading Feedback
**Learning:** For Multi-Page Applications (MPA), using `setTimeout(..., 0)` in a form submission handler is essential to allow the browser to initiate the POST request before the submit button is disabled. Additionally, using a 3px green box-shadow with `outline: 2px solid transparent` provides a highly visible focus state that respects high-contrast modes.
**Action:** Apply this pattern to all form-based interactive elements to ensure accessibility and clear user feedback.
