## 2025-05-14 - Loading State in Multi-Page Applications (MPAs)
**Learning:** In traditional form submissions (MPAs), disabling the submit button immediately in the 'submit' event listener can prevent the browser from successfully initiating the POST request.
**Action:** Use `setTimeout(..., 0)` to defer disabling the button until the next event loop tick, ensuring the form submission process has started.

## 2025-05-14 - Accessible Focus States for High Contrast
**Learning:** Using `outline: none` or just a `box-shadow` for focus states can make interactive elements invisible to users with high-contrast modes or screen readers that depend on system focus indicators.
**Action:** Use `outline: 2px solid transparent` in combination with a custom `box-shadow`. The transparent outline ensures the system still recognizes and highlights the element in high-contrast modes, while the box-shadow provides a modern visual style for others.
