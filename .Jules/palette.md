## 2026-05-06 - Initial UI Assessment
**Learning:** The initial interface is functional but lacks basic accessibility (no labels) and feedback for long-running operations (video generation).
**Action:** Always ensure forms have proper `<label>` elements and provide visual feedback for async tasks.

## 2026-05-06 - Testing Loading States
**Learning:** When testing form submission loading states in Playwright, using `page.evaluate` to add a `submit` listener that calls `e.preventDefault()` is a reliable way to keep the page from navigating, allowing for stable assertions on the temporary UI state (like disabled buttons or loading spinners).
**Action:** Use `e.preventDefault()` in verification scripts for async form feedback tests.
