## 2025-02-27 - [Immediate Submission Feedback]
**Learning:** For Multi-Page Applications (MPAs), using `setTimeout(..., 0)` when disabling a submit button on form submission is crucial to ensure the browser successfully initiates the POST request before the button enters a state that might block it.
**Action:** Always use the `setTimeout(..., 0)` pattern when adding loading states to standard HTML form buttons.

## 2025-02-27 - [Consistent Accessibility Markers]
**Learning:** Using a `.visually-hidden` class for form labels provides necessary context for screen readers without cluttering a minimalist visual design.
**Action:** Implement `.visually-hidden` for all inputs that lack a visible descriptive label.
