## 2025-05-14 - Loading State for Form Submissions
**Learning:** For Multi-Page Applications (MPAs) like this Flask app, providing immediate UI feedback during form submission (like disabling the button and showing 'Generating...') requires careful timing. Using `setTimeout(..., 0)` in the JavaScript submission handler ensures the browser's default form submission process starts before the button is disabled, which could otherwise prevent the request in some browsers.
**Action:** Always use `setTimeout(() => { btn.disabled = true; }, 0)` when disabling a submit button to provide UX feedback in standard form POSTs.

## 2025-05-14 - Accessible Focus States
**Learning:** Standard `outline: none` is detrimental to accessibility. A better approach is using `outline: 2px solid transparent` combined with a high-contrast-friendly `box-shadow` or `border-color` change to ensure focus visibility across all user environments, including high-contrast modes.
**Action:** Replace `outline: none` with transparent outlines and use multiple visual cues (shadow and border) for focus states.
