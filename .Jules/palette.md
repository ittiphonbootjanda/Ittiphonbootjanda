## 2025-05-21 - [UX] Reliable Submit Button Feedback in Vanilla HTML Forms
**Learning:** In simple HTML forms (like Flask templates), disabling a submit button immediately in an `onsubmit` handler can sometimes prevent the browser from successfully initiating the POST request. Using `setTimeout(() => { button.disabled = true }, 0)` ensures the browser's submission logic is triggered before the button becomes inactive.
**Action:** Use `setTimeout(..., 0)` when disabling submit buttons for loading states in non-SPA environments to ensure reliable form submission.

## 2025-05-21 - [A11y] Accessible Real-time Character Counters
**Learning:** For dynamic UI elements like character counters, using `aria-live="polite"` ensures screen readers announce updates without interrupting the user. Adding `aria-atomic="true"` ensures the entire counter (e.g., "15 / 500") is read rather than just the changed digit, providing full context.
**Action:** Always include `aria-live="polite"` and `aria-atomic="true"` on live metric displays to maintain accessibility.
