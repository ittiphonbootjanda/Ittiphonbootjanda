## 2025-05-14 - MPA Form Submission Feedback
**Learning:** In Multi-Page Applications (MPAs), using `setTimeout(..., 0)` in a form's `submit` event listener allows the browser to initiate the POST request before the submit button is disabled. This provides immediate visual feedback ("Generating...") without blocking the actual submission.
**Action:** Use `setTimeout(..., 0)` for submit button state changes in MPAs to ensure the request is sent while providing UX feedback.

## 2025-05-14 - Accessible Focus States
**Learning:** Standard browser outlines can be insufficient for accessibility, especially in high-contrast modes. A combination of `box-shadow` for visual flair and a transparent `outline` ensures the focus state is visible across all environments, including high-contrast mode where `box-shadow` might be ignored.
**Action:** Always pair `box-shadow` focus indicators with `outline: 2px solid transparent` and a high-contrast border color.
