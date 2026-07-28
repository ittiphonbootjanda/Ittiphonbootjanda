## 2025-05-22 - [Enhancing Form Feedback and Accessibility]
**Learning:** In traditional Flask applications where forms are submitted synchronously, browsers may prioritize navigation over UI updates. Using `setTimeout(..., 0)` in the `onsubmit` handler allows the browser to process UI changes (like disabling a button and updating its text) before the form submission blocks the main thread.
**Action:** Always wrap `this.submit()` in a `setTimeout` with 0 delay when performing immediate UI feedback on synchronous form submissions to ensure the "loading" state is visible to the user.
