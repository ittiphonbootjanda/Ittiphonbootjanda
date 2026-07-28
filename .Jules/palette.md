## 2025-05-15 - Immediate Feedback on Form Submission in MPAs

**Learning:** In Multi-Page Applications (MPAs), disabling a submit button immediately on the 'submit' event can sometimes prevent the browser from actually sending the POST request. Using `setTimeout(..., 0)` ensures the event loop completes the form submission trigger before the button state changes.

**Action:** Always wrap button disabling/loading text updates in a `setTimeout(..., 0)` within the submit event listener to guarantee reliable form submission while providing immediate UX feedback.
