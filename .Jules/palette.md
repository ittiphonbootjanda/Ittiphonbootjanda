## 2026-06-01 - [Loading Feedback Pattern for Simple Forms]
**Learning:** In simple HTML forms without AJAX, disabling a submit button immediately in the `onsubmit` handler can sometimes block the browser's form submission. Using `setTimeout(..., 0)` to defer the disabling and text change ensures the browser successfully initiates the POST request while still providing immediate visual feedback to the user.
**Action:** Use `onsubmit="setTimeout(() => { btn.disabled = true; }, 0)"` for non-AJAX form submissions to provide safe loading feedback.
