import pytest
from playwright.sync_api import Page, expect
import threading
import time
from app import app
import os

@pytest.fixture(scope="module", autouse=True)
def server():
    if not os.path.exists('videos'):
        os.makedirs('videos')
    if not os.path.exists('music'):
        os.makedirs('music')

    server_thread = threading.Thread(target=lambda: app.run(port=3000, debug=False, use_reloader=False))
    server_thread.daemon = True
    server_thread.start()

    time.sleep(2)
    yield

def test_ux_elements(page: Page):
    page.goto("http://localhost:3000")

    # Check for label
    label = page.locator('label.visually-hidden')
    expect(label).to_have_count(1)
    expect(label).to_have_text("Video Text Content")

    # Check for required textarea
    textarea = page.locator('textarea#text-input')
    expect(textarea).to_have_attribute("required", "")

    # Check for button
    button = page.locator('#submit-btn')
    expect(button).to_have_value("Generate Video")

def test_button_loading_js_logic(page: Page):
    page.goto("http://localhost:3000")

    # Trigger the submit event but prevent default to keep the page alive
    page.evaluate("""() => {
        const form = document.getElementById('video-form');
        form.addEventListener('submit', (e) => e.preventDefault(), { capture: true });
        form.dispatchEvent(new Event('submit', { cancelable: true }));
    }""")

    # Wait for the setTimeout(..., 0) in the app code
    page.wait_for_timeout(200)

    button = page.locator('#submit-btn')
    expect(button).to_be_disabled()
    expect(button).to_have_value("Generating...")

def test_accessibility_styles(page: Page):
    page.goto("http://localhost:3000")
    label = page.locator('label.visually-hidden')

    # Check that it has the visually-hidden styles
    styles = page.evaluate("""(el) => {
        const style = window.getComputedStyle(el);
        return {
            position: style.position,
            width: style.width,
            height: style.height,
            overflow: style.overflow
        };
    }""", label.element_handle())

    assert styles['position'] == 'absolute'
    assert styles['width'] == '1px'
    assert styles['height'] == '1px'
    assert styles['overflow'] == 'hidden'

def test_focus_styles(page: Page):
    page.goto("http://localhost:3000")
    textarea = page.locator('textarea#text-input')
    textarea.focus()

    box_shadow = page.evaluate("""(el) => window.getComputedStyle(el).boxShadow""", textarea.element_handle())
    # Should contain the rgba(76, 175, 80, 0.4)
    # Check for the values 76, 175, 80
    assert "76, 175, 80" in box_shadow
