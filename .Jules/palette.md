## 2025-05-14 - Loading State for Form Submissions
**Learning:** When disabling a submit button on form submission to provide UX feedback, using `setTimeout(..., 0)` in the JavaScript handler ensures the browser successfully initiates the POST request before the button enters the disabled state.
**Action:** Always wrap `submitBtn.disabled = true` in a `setTimeout` when triggered by the form's `submit` event.

## 2025-05-14 - Real-time Character Counters
**Learning:** Dynamic UI elements that provide real-time feedback, such as character counters, should include the `aria-live="polite"` attribute to ensure screen reader users receive updates as they interact with the element.
**Action:** Use `aria-live="polite"` on feedback elements like character counters and initialize them on load to handle pre-filled data.

## 2025-05-14 - Accessible Focus States
**Learning:** High-visibility focus states (e.g., using `box-shadow` and `border`) should be used with `:focus-visible` to ensure keyboard users can navigate easily, while `outline: 2px solid transparent` helps maintain visibility in high-contrast modes.
**Action:** Use a combination of `border-color` and `box-shadow` for focus states, and ensure `outline` is handled for high-contrast accessibility.
