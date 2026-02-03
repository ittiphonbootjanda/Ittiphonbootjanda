## 2026-02-03 - [Accessibility & Feedback]
**Learning:** Simple HTML forms often lack proper labels and focus states, hindering accessibility. Additionally, long-running processes like video generation require immediate UI feedback to prevent double-submissions and improve user confidence.
**Action:** Always include .visually-hidden labels for form fields and use a JavaScript submission handler to disable the submit button and show a "Processing..." state using the setTimeout(..., 0) pattern.
