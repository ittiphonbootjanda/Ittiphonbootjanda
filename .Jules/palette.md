## 2025-05-14 - Loading states in Multi-Page Applications
**Learning:** For long-running server-side actions in MPAs, providing immediate UI feedback (like disabling the submit button) requires careful timing. Using `setTimeout(..., 0)` in the submit event listener ensures the browser initiates the form submission before the button becomes disabled, which might otherwise block the request in some browsers.
**Action:** Always use `setTimeout(..., 0)` when disabling a submit button in an MPA to ensure smooth user feedback without interrupting the navigation.

## 2025-05-14 - Verifying Visually Hidden Elements
**Learning:** Playwright's `to_be_hidden()` assertion checks for `display: none` or `visibility: hidden`. Elements with the `.visually-hidden` class (using 1x1 size and absolute positioning) are still considered "visible" by Playwright.
**Action:** Verify accessible but visually hidden elements by checking for the specific utility class or text content instead of using visibility-based assertions.
