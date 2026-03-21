## 2024-05-24 - [Submit Button UX Feedback]
**Learning:** Using `setTimeout(..., 0)` in a form submission handler allows the browser to initiate the POST request before the button is disabled, ensuring navigation still occurs while providing immediate visual feedback.
**Action:** Use this pattern to improve the user experience for long-running form actions in MPAs.

## 2024-05-24 - [Accessibility with Visually Hidden Labels]
**Learning:** Providing explicit labels for all form fields, even when they seem self-explanatory through placeholders, is crucial for screen reader users. The `.visually-hidden` class allows these labels to be accessible without affecting the visual layout.
**Action:** Always include associated labels for form inputs, utilizing a utility class for visual hiding when necessary.
