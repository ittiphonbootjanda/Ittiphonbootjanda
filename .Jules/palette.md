## 2026-01-30 - [Loading State Feedback]
**Learning:** Long-running backend processes like video generation require immediate UI feedback to prevent user frustration and duplicate submissions.
**Action:** Use a simple JavaScript 'submit' listener to disable the submit button and update its text to 'Generating...'. Ensure a .visually-hidden label is present for accessibility when using placeholders.
