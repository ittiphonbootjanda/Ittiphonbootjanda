## 2025-05-22 - [Transient UI States and Video Generation]
**Learning:** For long-running operations like video generation that block the UI, provide immediate visual feedback (disabling buttons, changing text) to prevent duplicate submissions and manage user expectations.
**Action:** Use an onsubmit handler with a short delay (setTimeout 0) to update the UI state before the browser initiates the request.
