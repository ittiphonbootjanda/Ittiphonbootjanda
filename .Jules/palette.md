## 2025-05-14 - Loading state for long-running form submissions
**Learning:** For Multi-Page Applications (MPAs) where a form submission triggers a slow backend process (like video generation), providing immediate visual feedback is crucial. Using `setTimeout(..., 0)` in a `submit` event listener allows the browser to initiate the POST request before the submit button is disabled, preventing double-submissions while keeping the user informed.
**Action:** Always implement a loading state for form-based async-like operations, ensuring the button's text updates and its style reflects an inactive state with sufficient contrast.

## 2025-05-14 - Testing visually hidden elements and transitions
**Learning:** Standard Playwright checks like `to_be_hidden()` can be misleading for `.visually-hidden` elements which are technically "visible" to the DOM and screen readers but hidden from the visual viewport. Also, computed style assertions for CSS transitions require a small `wait_for_timeout` to ensure the final state is captured.
**Action:** Use `to_be_visible()` but verify the `.visually-hidden` class for screen-reader-only elements, and always include a short delay (e.g., 300ms) before checking computed styles of transitioning elements.
