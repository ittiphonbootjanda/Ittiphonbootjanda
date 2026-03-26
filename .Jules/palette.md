## 2025-05-15 - [Button Loading State in MPAs]
**Learning:** In Multi-Page Applications (MPAs), disabling a submit button immediately in the `submit` event handler can sometimes prevent the browser from actually sending the POST request.
**Action:** Use `setTimeout(fn, 0)` to defer disabling the button until the next event loop tick, ensuring the form submission is successfully initiated by the browser while still providing immediate visual feedback to the user.

## 2025-05-15 - [Accessible Hidden Labels]
**Learning:** For inputs that don't have a visual label for design reasons, a `.visually-hidden` class is essential to provide context to screen reader users without affecting the visual layout.
**Action:** Always include a `<label>` with a `.visually-hidden` class for all form inputs to ensure WCAG compliance and a better experience for assistive technology users.
