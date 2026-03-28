## 2025-05-15 - [Loading State for MPA Form Submission]
**Learning:** When disabling a submit button on form submission in a Multi-Page Application (MPA) to provide UX feedback, using `setTimeout(..., 0)` in the JavaScript handler ensures the browser successfully initiates the POST request before the button enters the disabled state. Without this, some browsers might cancel the request if the button is disabled too quickly.
**Action:** Always wrap submit button disabling logic in `setTimeout(..., 0)` for standard HTML form submissions.

## 2025-05-15 - [Accessible Focus States with High Contrast Support]
**Learning:** To ensure focus states are visible even in high-contrast modes, replacing `outline: none` with `outline: 2px solid transparent` allows the browser's high-contrast styles to override the transparency while maintaining a custom design in standard modes.
**Action:** Use `outline: 2px solid transparent` and `box-shadow` for custom focus indicators.
