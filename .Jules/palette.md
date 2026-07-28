## 2025-05-14 - Loading states in Multi-Page Applications (MPA)
**Learning:** In traditional HTML forms (MPA), disabling a submit button immediately in the `submit` event handler can sometimes prevent the browser from actually sending the POST request. Using `setTimeout(..., 0)` ensures the browser initiates the request before the button state changes.
**Action:** Always use `setTimeout(fn, 0)` when disabling submit buttons on form submission to provide UX feedback without breaking the request.

## 2025-05-14 - Verifying transitions in Playwright
**Learning:** When testing focus states or other interactive changes that use CSS transitions, computed styles (like `box-shadow`) may not immediately reflect the final state.
**Action:** Include a small wait (e.g., 300ms) after triggering the interaction in Playwright before asserting on computed CSS properties that are animated.
