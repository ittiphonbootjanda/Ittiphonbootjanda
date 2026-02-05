## 2025-02-05 - [Consistent Loading State & Accessibility Pattern]
**Learning:** For long-running server-side tasks (like video generation), providing immediate UI feedback via a disabled "Generating..." state is critical to prevent duplicate submissions and manage user expectations. Combining this with a .visually-hidden label and custom focus rings ensures the UX is both pleasant and accessible.
**Action:** Always implement a submission handler that disables the button and provides visual feedback for form-based async-like actions. Use the standard 3px green box-shadow for focus states.
