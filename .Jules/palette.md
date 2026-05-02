## 2026-05-02 - [Accessible Real-time Feedback & Clean Repo Hygiene]
**Learning:** Dynamic UI elements like character counters should use `aria-live="polite"` to be accessible to screen reader users. Additionally, when working in an environment without a `.gitignore`, it's critical to manually clean up `__pycache__`, logs, and temporary verification artifacts before submission to maintain repository health.
**Action:** Always add `aria-live="polite"` to live-updating text elements and include a cleanup step in the plan for any temporary files created.
