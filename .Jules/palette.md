## 2025-05-15 - Improving slow process feedback with loading states
**Learning:** For asynchronous tasks that take several seconds (like video generation), users need immediate visual feedback to know the process has started and to prevent double-submissions. Disabling the submit button and changing its text is a low-effort, high-impact pattern.
**Action:** Always implement loading states on buttons for long-running form submissions.

## 2025-05-15 - Non-disruptive accessibility labels
**Learning:** Using a `.visually-hidden` class allows adding descriptive `<label>` elements for screen readers without altering the visual design, ensuring WCAG compliance while maintaining the intended aesthetic.
**Action:** Use `.visually-hidden` labels for inputs where the visual design implies the purpose but an explicit label is missing.
