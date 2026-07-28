## 2025-05-15 - Improving Form Submission Feedback in MPAs
**Learning:** In Multi-Page Applications (MPAs), disabling a submit button immediately on click can sometimes prevent the browser from correctly initiating the POST request. Using `setTimeout(..., 0)` allows the event loop to process the form submission before the button enters a disabled state, ensuring a smooth transition to the loading UI.
**Action:** Always wrap submit button state changes (disabling/text updates) in a `setTimeout(..., 0)` when working with standard HTML form submissions.
