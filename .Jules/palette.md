## 2025-05-14 - [Testing loading states in MPAs]
**Learning:** When verifying UI state changes triggered by form submission in a Multi-Page Application (MPA), use `page.evaluate` to add a `submit` event listener that calls `e.preventDefault()`. This allows verification of the immediate UI state (e.g., button disabling) before navigation occurs.
**Action:** Use `e.preventDefault()` in Playwright tests to reliably capture transient UI states before form navigation.
