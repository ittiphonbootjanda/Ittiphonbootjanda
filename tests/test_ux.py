import pytest
from playwright.sync_api import Page, expect
import os
import signal
import subprocess
import time
import requests

@pytest.fixture(scope="module", autouse=True)
def server():
    # Start the Flask app without debug mode to avoid Pin screen if possible
    # Setting FLASK_DEBUG=0 or just not passing debug=True in app.run
    # But app.py has app.run(debug=True, port=3000)

    # We can try to monkeypatch or just let it be.
    # Actually, the Pin screen only shows on errors.

    proc = subprocess.Popen(["python", "app.py"], env=dict(os.environ, FLASK_DEBUG="0"), stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Wait for the server to be ready
    timeout = 10
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            # Explicitly use 127.0.0.1 to avoid localhost issues
            response = requests.get("http://127.0.0.1:3000")
            if response.status_code == 200:
                break
        except requests.exceptions.ConnectionError:
            time.sleep(0.5)

    yield

    # Clean up the process
    subprocess.run("fuser -k 3000/tcp", shell=True)
    os.kill(proc.pid, signal.SIGTERM)

def test_index_page_has_label(page: Page):
    page.goto("http://127.0.0.1:3000")
    # Check if there is a label for the textarea
    label = page.locator("label[for='text']")
    # This is expected to fail initially as there is no label
    expect(label).to_be_visible()

def test_submit_button_loading_state(page: Page):
    page.goto("http://127.0.0.1:3000")
    # Ensure we are not on the PIN screen
    expect(page.locator("h1")).to_have_text("Text to Video Generator")

    textarea = page.locator("textarea[name='text']")
    textarea.fill("Test text for video")

    submit_button = page.locator("input[type='submit']")

    # To check the immediate UI change, we can prevent navigation
    page.evaluate("""
        document.querySelector('form').addEventListener('submit', (e) => {
            e.preventDefault();
        });
    """)

    submit_button.click()

    # This is expected to fail initially as there is no JS handling the loading state
    expect(submit_button).to_have_value("Generating...")
    expect(submit_button).to_be_disabled()
