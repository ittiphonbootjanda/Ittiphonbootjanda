## 2025-05-14 - Loading States in Multi-Page Applications (MPAs)
**Learning:** When using JavaScript to provide immediate feedback on form submission (like disabling a button) in a standard HTML form (MPA), wrap the state change in a `setTimeout(..., 0)`. This ensures the browser registers the form submission and initiates the POST request before the element is disabled, avoiding potential race conditions that could cancel the submission.
**Action:** Use the `setTimeout(..., 0)` pattern for button disabling on submit to ensure reliable UX feedback without breaking native browser behavior.
