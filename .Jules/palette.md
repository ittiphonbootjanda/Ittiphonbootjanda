## 2026-02-10 - [Button Disabling Pattern]
**Learning:** When disabling a submit button on form submission to provide UX feedback, use `setTimeout(..., 0)`. This ensures the browser successfully initiates the POST request before the button enters the disabled state, which otherwise might prevent the submission in some browsers.
**Action:** Always wrap `btn.disabled = true` in a `setTimeout` with 0ms delay inside the submit event listener.
