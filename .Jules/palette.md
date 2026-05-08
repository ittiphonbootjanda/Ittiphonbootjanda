## 2025-05-14 - Loading State for native forms
**Learning:** When using native form submission in a multi-page app, disabling the submit button immediately in the 'submit' event can prevent the browser from actually sending the POST request in some engines.
**Action:** Use `setTimeout(..., 0)` to defer disabling the button until the next tick, ensuring the form submission is initiated by the browser.
