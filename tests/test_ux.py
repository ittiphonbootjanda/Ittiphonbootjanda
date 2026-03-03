import pytest
from playwright.sync_api import Page, expect

def test_index_page_loads(page: Page):
    page.goto("http://localhost:3000")
    expect(page.get_by_role("heading", name="Text to Video Generator")).to_be_visible()

def test_form_accessibility(page: Page):
    page.goto("http://localhost:3000")
    # Check if textarea has a properly associated label
    textarea = page.locator("#text-input")
    expect(textarea).to_be_visible()

    # Check for associated label by its text content which is visually hidden
    label = page.get_by_text("Text to convert into video")
    expect(label).to_be_attached()
    # It should have class visually-hidden
    expect(label).to_have_class("visually-hidden")

def test_loading_state(page: Page):
    page.goto("http://localhost:3000")
    textarea = page.locator("#text-input")
    textarea.fill("Hello world")

    submit_button = page.locator("#submit-button")

    # Prevent navigation to verify intermediate UI state
    page.evaluate("""
        document.getElementById('generator-form').addEventListener('submit', (e) => {
            e.preventDefault();
        });
    """)

    submit_button.click()

    # Wait for the setTimeout(..., 0) in the app code to fire
    page.wait_for_timeout(100)

    # Check if button text changed to "Generating..."
    expect(submit_button).to_have_value("Generating...")
    # Check if button is disabled
    expect(submit_button).to_be_disabled()

def test_textarea_required(page: Page):
    page.goto("http://localhost:3000")
    textarea = page.locator("#text-input")
    expect(textarea).to_have_attribute("required", "")
