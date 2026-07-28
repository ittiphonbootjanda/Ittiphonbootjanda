## 2026-04-06 - [Loading Feedback in MPAs]
**Learning:** When adding a loading state (disabling button) to a native HTML form submit in an MPA, using `setTimeout(..., 0)` ensures the browser successfully initiates the POST request before the button enters the disabled state, which might otherwise cancel the navigation in some browsers.
**Action:** Always wrap button disabling logic in a `setTimeout(..., 0)` for native form submissions.

## 2026-04-06 - [Accessible Disabled States]
**Learning:** To meet WCAG contrast standards for disabled buttons with white text, using a dark background (e.g., `#2e7d32`) with reduced opacity (e.g., `0.7`) and translucent white text (e.g., `rgba(255, 255, 255, 0.7)`) maintains a visible 4.5:1 ratio while clearly signaling the interactive state change.
**Action:** Use high-contrast base colors for disabled states combined with opacity rather than just light gray.
