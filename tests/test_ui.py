import pytest
from playwright.sync_api import Page, expect
import threading
import time
import os
from app import app

def run_app():
    # Use a different port for testing to avoid conflicts
    app.run(port=3001, debug=False, use_reloader=False)

@pytest.fixture(scope="module", autouse=True)
def server():
    thread = threading.Thread(target=run_app)
    thread.daemon = True
    thread.start()
    time.sleep(2)  # Give the server more time to start
    yield

def test_ui_elements(page: Page):
    page.goto("http://localhost:3001")

    # Check label exists and is visually hidden
    label = page.locator('label[for="video-text"]')
    expect(label).to_have_count(1)
    expect(label).to_have_class("visually-hidden")
    expect(label).to_have_text("Video Text")

    # Check textarea has correct id and is required
    textarea = page.locator('#video-text')
    expect(textarea).to_have_attribute("required", "")

    # Check submit button
    submit_btn = page.locator('input[type="submit"]')
    expect(submit_btn).to_have_value("Generate Video")

def test_loading_state(page: Page):
    page.goto("http://localhost:3001")

    textarea = page.locator('#video-text')
    textarea.fill("Test video content")

    submit_btn = page.locator('input[type="submit"]')

    # Use the pattern from memory: prevent navigation to check immediate UI state
    page.evaluate("""
        document.querySelector('form').addEventListener('submit', (e) => {
            // We want our original listener to run first to set the state,
            // but we want to prevent the actual navigation/submission.
            // Our script uses setTimeout(..., 0) for this.submit(),
            // so if we preventDefault here, it might still try to submit later.
            // Let's also mock HTMLFormElement.prototype.submit
            window._formSubmitted = true;
        }, { capture: true });
        HTMLFormElement.prototype.submit = function() {
            window._formSubmitCalled = true;
        };
    """)

    submit_btn.click()

    # Verify button is disabled and text changed
    expect(submit_btn).to_be_disabled()
    expect(submit_btn).to_have_value("Generating...")

def test_focus_styles(page: Page):
    page.goto("http://localhost:3001")
    textarea = page.locator('#video-text')

    # Focus the textarea
    textarea.focus()

    # Wait a bit for transitions
    page.wait_for_timeout(300)

    # Check computed styles for box-shadow
    box_shadow = textarea.evaluate("el => window.getComputedStyle(el).boxShadow")
    assert "rgba(76, 175, 80, 0.4)" in box_shadow or "rgba(76, 175, 80, 0.4)" in box_shadow.replace(" ", "")
