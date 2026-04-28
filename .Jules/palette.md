## 2025-05-14 - [Form Submission Feedback Pattern]
**Learning:** In Multi-Page Applications (MPAs), disabling a submit button immediately upon submission can sometimes prevent the browser from actually sending the POST request. Using `setTimeout(..., 0)` in the submit handler ensures the event loop processes the submission before the button becomes disabled.
**Action:** Always wrap submit button disabling logic in `setTimeout(..., 0)` for vanilla JS form handlers.

## 2025-05-14 - [Accessible Focus States]
**Learning:** Default browser outlines can be inconsistent or hard to see. A combination of `outline: 2px solid transparent` (for high-contrast mode compatibility) and a tailored `box-shadow` provides a clear, visually pleasing focus state that follows the component's border radius.
**Action:** Use `box-shadow` for focus rings and ensure `outline` is not completely removed but set to transparent.
