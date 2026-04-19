## 2025-05-14 - Loading State for Form Submissions
**Learning:** For Multi-Page Applications (MPAs), immediate visual feedback on form submission is crucial to prevent double submissions and clarify that the process has started, especially for long-running tasks like video generation. Using `setTimeout(..., 0)` in the submit handler ensures the browser can still process the POST request before the button is disabled.
**Action:** Always provide a 'Processing...' state for long-running form submissions.

## 2025-05-14 - Focus States and Transitions
**Learning:** A clear focus ring (e.g., 3px spread box-shadow) combined with a subtle border color change significantly improves keyboard navigation visibility. Adding a short transition (0.2s) makes the interaction feel much more polished and intentional.
**Action:** Use `rgba` shadows and border color changes for focus states with `transition: all 0.2s`.
