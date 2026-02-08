## 2025-01-29 - Form Submission Feedback Pattern
**Learning:** When generating content server-side (like video), providing a "Generating..." state with a disabled button prevents duplicate submissions and reduces user anxiety during long-running processes. Using `setTimeout(fn, 0)` is essential to ensure the form submission initiates before the button is disabled.
**Action:** Always implement immediate visual feedback for form submissions that trigger long-running backend tasks.

## 2025-01-29 - Accessibility in Minimalist UIs
**Learning:** Minimalist interfaces often omit labels in favor of placeholders, which breaks screen reader support. The `.visually-hidden` pattern is a perfect compromise to maintain the aesthetic while meeting accessibility standards.
**Action:** Use `.visually-hidden` labels for all inputs that rely on placeholders for their visual context.
