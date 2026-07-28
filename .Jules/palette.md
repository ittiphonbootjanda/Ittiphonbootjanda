## 2026-05-10 - [Playwright Visibility and Visually-Hidden Utility]
**Learning:** Elements styled with the standard `.visually-hidden` utility (absolute positioning, 1x1px size, etc.) are often reported as "visible" by Playwright's `expect(locator).to_be_visible()` because they are technically in the DOM and have a non-zero size.
**Action:** To verify an element is visually hidden, use a bounding box check `assert box['width'] <= 1 and box['height'] <= 1` or check for the specific CSS properties, rather than relying on standard visibility assertions.

## 2026-05-10 - [Stable Loading State Snapshots]
**Learning:** Capturing stable snapshots of transient UI states (like a button becoming "Generating...") during form submission can be tricky if the page reloads too quickly.
**Action:** Use `page.evaluate` to trigger a `submit` event or use a mock listener that prevents default to hold the UI in the "loading" state for verification, or use `setTimeout(..., 0)` in the application code to ensure the state change is visible before the browser starts navigation.
