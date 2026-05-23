## 2025-05-22 - [Refining Micro-UX and Feedback Loops]

**Learning:** Micro-UX enhancements like real-time character counters and loading states significantly improve perceived performance and accessibility. Using `aria-live="polite"` with `aria-atomic="true"` ensures that screen readers provide useful, non-disruptive context for dynamic updates.

**Action:** Always include immediate visual and aria-live feedback for long-running operations and limited-length inputs. Use `document.getElementById` for inline JavaScript to ensure maintainability and stability across browsers.
