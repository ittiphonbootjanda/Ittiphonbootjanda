## 2025-05-15 - [Accessible Loading State]
**Learning:** For submit buttons, a disabled state with a light background and white text often fails WCAG AA contrast standards. Using a darker background (e.g., `#2e7d32`) with a subtle opacity change (0.7) and translucent white text (`rgba(255,255,255,0.7)`) provides a better balance of showing the 'disabled' state while maintaining readable contrast.
**Action:** Always verify contrast ratios for disabled states, especially when using primary brand colors as backgrounds.

## 2025-05-15 - [MPA Loading UI]
**Learning:** In Multi-Page Applications (MPAs), using `setTimeout(..., 0)` to disable a submit button ensures the browser initiates the form submission before the UI state changes. This prevents blocking the request while giving immediate user feedback.
**Action:** Use the `setTimeout(..., 0)` pattern for simple MPA form feedback to avoid race conditions.
