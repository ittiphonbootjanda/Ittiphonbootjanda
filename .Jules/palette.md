# Palette's Journal

## 2025-03-08 - Loading state feedback for long-running operations
**Learning:** For long-running server-side operations (like video generation), users need immediate feedback to know their request is being processed. Disabling the submit button prevents multiple submissions and provides a clear "work in progress" signal. Using `setTimeout(..., 0)` ensures the browser initiates the POST request before the button state changes.
**Action:** Always implement a loading state for form submissions that trigger time-consuming tasks.

## 2025-03-08 - Accessible labels for clean designs
**Learning:** Even when a design doesn't visually require a label (e.g., when a placeholder or heading provides context), a semantic `<label>` is essential for screen readers. Using a `.visually-hidden` utility class allows for a clean visual design while maintaining full accessibility.
**Action:** Include `<label>` elements for all form inputs, using `.visually-hidden` if they shouldn't be visible.
