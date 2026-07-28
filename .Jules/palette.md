# Palette's UX Journal

## 2026-03-13 - [Loading State for Video Generation]
**Learning:** For long-running operations like video generation, users need immediate visual feedback to confirm their action was registered. Disabling the submit button prevents duplicate submissions and changing the button text provides clear status communication.
**Action:** Always implement a JavaScript handler for forms triggering heavy backend tasks to disable the submit button and show a "Processing..." state.
