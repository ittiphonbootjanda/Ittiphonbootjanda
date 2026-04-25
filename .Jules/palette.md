## 2025-04-25 - [Immediate UI Feedback in Flask/MPA]
**Learning:** In a traditional Multi-Page Application (MPA) like this Flask app, disabling a submit button immediately in a 'submit' event listener can sometimes prevent the browser from actually sending the POST request.
**Action:** Use `setTimeout(() => { button.disabled = true; }, 0)` in the submit handler. This ensures the browser's form submission process is initiated before the DOM element becomes inactive.
