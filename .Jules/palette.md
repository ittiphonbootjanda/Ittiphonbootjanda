## 2025-05-22 - [Form Submission Feedback]
**Learning:** For long-running server actions (like video generation), users need immediate visual feedback to prevent double-clicks and reduce perceived wait time. Using `setTimeout(..., 0)` allows the form submission to initiate before the button is disabled.
**Action:** Always implement a disabled loading state on submit buttons for async or long-running tasks.

## 2025-05-22 - [Accessible Character Counters]
**Learning:** Character counters provide essential context for length-limited inputs. Using `aria-live="polite"` and `aria-atomic="true"` ensures screen readers announce the full context (e.g., "47 / 500") rather than just the changing digits.
**Action:** Pair `maxlength` with a live-region character counter for better accessibility.
