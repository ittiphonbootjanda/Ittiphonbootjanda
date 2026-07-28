## 2026-05-30 - Enhanced Focus States and Real-time Feedback
**Learning:** For long-running operations like FFmpeg video generation, immediate visual feedback (e.g., disabling the submit button and changing its text) is crucial to prevent multiple submissions and improve perceived performance. Additionally, using `box-shadow` for focus rings prevents layout shifts that occur when adding borders to focused elements.
**Action:** Always implement loading states for slow form submissions and prefer `box-shadow` for focus indicators to maintain layout stability.

## 2026-05-30 - Visually Hidden Labels for Accessibility
**Learning:** Screen readers need `<label>` elements even if they aren't part of the visual design. The `.visually-hidden` utility pattern is a reliable way to provide this context without affecting the UI layout.
**Action:** Use a `.visually-hidden` class for form labels that should not be visible but must remain accessible.
