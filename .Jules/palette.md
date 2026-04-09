## 2025-05-14 - Loading State Pattern in MPAs
**Learning:** In Multi-Page Applications (MPAs), using `setTimeout(..., 0)` when disabling a submit button on form submission ensures the browser initiates the POST request before the element becomes inactive.
**Action:** Always wrap `button.disabled = true` in a `setTimeout` or `requestAnimationFrame` when triggered by a `submit` event.

## 2025-05-14 - Focus States for Accessibility
**Learning:** Using a combination of `box-shadow` and a solid `border` provides high-visibility focus indicators that work well across different browser high-contrast modes.
**Action:** Use `box-shadow: 0 0 0 3px rgba(76, 175, 80, 0.4); border-color: #2e7d32; outline: 2px solid transparent;` for focus states.
