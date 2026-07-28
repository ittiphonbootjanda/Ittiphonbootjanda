## 2025-05-15 - [Form Submission Loading State in MPAs]
**Learning:** In Multi-Page Applications (MPAs), disabling a submit button immediately in the `submit` event handler can sometimes prevent the browser from actually sending the POST request.
**Action:** Use `setTimeout(() => { button.disabled = true; }, 0)` to ensure the browser has queued the form submission before the UI state changes to disabled.

## 2025-05-15 - [Accessible Character Counters]
**Learning:** Real-time feedback like character counters must be announced to screen reader users to be truly useful and accessible.
**Action:** Use `aria-live="polite"` on the counter element so updates are announced as the user types without interrupting their flow.
