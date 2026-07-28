## 2026-03-16 - [UX/Interaction] Loading State in Multi-Page Applications (MPAs)
**Learning:** When disabling a submit button in a standard HTML form to provide immediate feedback, the browser may skip the form submission if the button is disabled synchronously.
**Action:** Use `setTimeout(..., 0)` in the submission handler to ensure the browser successfully initiates the POST request before the button enters the disabled state.

## 2026-03-16 - [Accessibility] Screen Reader Labels for Visual-Only Designs
**Learning:** For minimal designs where visual labels might be excluded, screen readers still require descriptive labels for form inputs.
**Action:** Use a `.visually-hidden` utility class to provide semantic `<label>` elements that are accessible to AT but hidden from sighted users.
