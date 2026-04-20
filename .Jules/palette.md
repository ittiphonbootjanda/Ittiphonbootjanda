## 2025-05-14 - [Form Feedback Pattern]
**Learning:** For long-running operations in an MPA, use `setTimeout(..., 0)` in the form's `submit` event listener to disable the button. This ensures the browser captures the form submission before the button is disabled, which can otherwise prevent the POST request in some browsers.
**Action:** Use `setTimeout(..., 0)` when disabling submit buttons on form submission to maintain reliable UX feedback without breaking navigation.

## 2025-05-14 - [Focus State Contrast]
**Learning:** To ensure visibility in high-contrast modes and provide a clear indicator, combine `box-shadow` with a solid `border` and set `outline: 2px solid transparent`.
**Action:** Apply the `outline: 2px solid transparent` pattern to interactive elements for better accessibility compliance.
