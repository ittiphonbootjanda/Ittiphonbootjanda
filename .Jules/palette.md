## 2025-05-14 - Loading state for MPA form submissions
**Learning:** When disabling a submit button on form submission to provide UX feedback in a Multi-Page Application (MPA), using `setTimeout(..., 0)` in the JavaScript handler ensures the browser successfully initiates the POST request before the button enters the disabled state. This prevents some browsers from cancelling the navigation if the button is disabled immediately.
**Action:** Always wrap the button-disabling logic in a `setTimeout` with a 0ms delay when handling form `submit` events.
