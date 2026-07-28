import pytest
from playwright.sync_api import Page, expect

def test_index_page_loads(page: Page):
    page.goto("http://localhost:3000")
    expect(page).to_have_title("Text to Video")
    expect(page.locator("h1")).to_contain_text("Text to Video Generator")

def test_form_has_required_elements(page: Page):
    page.goto("http://localhost:3000")
    # Check for textarea with label
    textarea = page.locator("textarea#text-input")
    expect(textarea).to_be_visible()
    expect(textarea).to_have_attribute("required", "")

    # Check for visually hidden label
    label = page.locator("label.visually-hidden")
    expect(label).to_have_text("Text to convert into video")

    # Check for submit button
    submit_button = page.locator("input[type='submit']")
    expect(submit_button).to_be_visible()

def test_loading_state_on_submit(page: Page):
    page.goto("http://localhost:3000")

    # Add a submit event listener to prevent navigation
    page.evaluate("""
        document.getElementById('generate-form').addEventListener('submit', (e) => {
            e.preventDefault();
        });
    """)

    textarea = page.locator("textarea#text-input")
    textarea.fill("Hello world")

    submit_button = page.locator("input[type='submit']")
    submit_button.click()

    # Wait for the setTimeout(..., 0) in the app's JS
    page.wait_for_timeout(100)

    # Now check if button is disabled and text changed
    expect(submit_button).to_be_disabled()
    expect(submit_button).to_have_value("Generating...")
