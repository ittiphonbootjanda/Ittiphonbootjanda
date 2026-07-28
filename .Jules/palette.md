## 2025-05-15 - [Immediate Loading Feedback for MPAs]
**Learning:** When using form submission in a Multi-Page Application (MPA), disabling the submit button immediately in a 'submit' event handler can prevent the form from actually being sent by the browser.
**Action:** Use `setTimeout(..., 0)` in the form submission handler to ensure the browser has successfully initiated the POST request before the button enters the disabled state.

## 2025-05-15 - [Screen Reader Accessibility for Hidden Labels]
**Learning:** For inputs with clear placeholder text, use a `.visually-hidden` CSS class to provide a semantic label for screen readers without cluttering the visual UI.
**Action:** Always pair this with an `aria-label` or an associated `<label>` with the `visually-hidden` class to meet accessibility standards.
