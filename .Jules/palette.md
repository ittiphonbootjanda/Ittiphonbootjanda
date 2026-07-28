## 2025-05-15 - [Pattern: Placeholders as Labels]
**Learning:** The application initially relied on `placeholder` attributes for input descriptions, which is an accessibility anti-pattern as they disappear on focus and are not always reliably announced by screen readers.
**Action:** Always provide a semantic `<label>` for every input. Use the `.visually-hidden` class if the label shouldn't be visible in the UI but needs to be accessible.
