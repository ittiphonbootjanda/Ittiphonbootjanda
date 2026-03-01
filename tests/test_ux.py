import pytest
from playwright.sync_api import Page, expect
import os
import signal
import subprocess
import time

@pytest.fixture(scope="module", autouse=True)
def server():
    # Start the Flask app
    process = subprocess.Popen(
        ["python", "app.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        preexec_fn=os.setsid
    )
    # Wait for the server to start by polling
    start_time = time.time()
    while time.time() - start_time < 10:
        try:
            import socket
            with socket.create_connection(("localhost", 3000), timeout=1):
                break
        except (OSError, ConnectionRefusedError):
            time.sleep(0.5)
    else:
        # Check if process is still running
        if process.poll() is not None:
            stdout, stderr = process.communicate()
            pytest.fail(f"Server failed to start. stdout: {stdout.decode()}, stderr: {stderr.decode()}")
        pytest.fail("Server did not start in time")

    yield
    # Kill the server
    os.killpg(os.getpgid(process.pid), signal.SIGTERM)

def test_index_page_loads(page: Page):
    page.goto("http://localhost:3000")
    expect(page).to_have_title("Text to Video")
    expect(page.locator("h1")).to_have_text("Text to Video Generator")

def test_accessibility_labels(page: Page):
    page.goto("http://localhost:3000")
    # Check for the visually-hidden label
    label = page.locator("label.visually-hidden")
    expect(label).to_have_text("Text to convert into video")
    # Verify it's associated with the textarea
    textarea = page.locator("#text-input")
    expect(textarea).to_be_visible()
    expect(textarea).to_have_attribute("required", "")

def test_loading_state(page: Page):
    page.goto("http://localhost:3000")

    # Fill the textarea
    page.fill("#text-input", "Test video content")

    # Use evaluate to add a submit listener that prevents default, so we can check the button state
    page.evaluate("""
        document.getElementById('generate-form').addEventListener('submit', (e) => {
            // We don't preventDefault here because we want to see the setTimeout effect
            // Actually, if we want to reliably catch the state BEFORE navigation,
            // preventing default is better for the test.
            // But our JS uses setTimeout(..., 0), so it might still run.
        });
    """)

    # Let's try to catch it by preventing navigation
    page.evaluate("""
        const form = document.getElementById('generate-form');
        form.onsubmit = (e) => {
            // The existing listener will still run and set the timeout
        };
    """)

    # Better yet, let's just use a more robust way to test the JS interaction
    # We'll prevent the actual submission to stay on the page
    page.evaluate("document.getElementById('generate-form').addEventListener('submit', e => e.preventDefault())")

    page.click("#submit-btn")

    # The setTimeout(..., 0) will run in the next tick
    # We might need a tiny wait
    page.wait_for_timeout(100)

    # Check if the button is disabled and text changed
    submit_btn = page.locator("#submit-btn")
    expect(submit_btn).to_be_disabled()
    expect(submit_btn).to_have_value("Generating...")

def test_focus_styles(page: Page):
    page.goto("http://localhost:3000")
    textarea = page.locator("#text-input")
    textarea.focus()

    # Wait for transition
    page.wait_for_timeout(300)

    # Check computed style for box-shadow
    box_shadow = textarea.evaluate("el => window.getComputedStyle(el).boxShadow")
    assert "rgba(76, 175, 80, 0.4)" in box_shadow or "rgb(76, 175, 80)" in box_shadow
