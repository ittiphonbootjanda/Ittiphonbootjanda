import pytest
from playwright.sync_api import expect

def test_ux_elements(page):
    page.goto("http://localhost:3000")

    # Check for the visually-hidden label
    label = page.locator('label[for="text-input"]')
    expect(label).to_have_class("visually-hidden")
    expect(label).to_have_text("Video Text Content")

    # Check for required textarea
    textarea = page.locator("#text-input")
    expect(textarea).to_have_attribute("required", "")

    # Check focus state for textarea (visual check)
    textarea.focus()
    page.wait_for_timeout(300) # Wait for transition
    box_shadow = textarea.evaluate("el => getComputedStyle(el).boxShadow")
    assert "rgba(76, 175, 80, 0.4)" in box_shadow or "rgba(76, 175, 80" in box_shadow

def test_loading_state(page):
    page.goto("http://localhost:3000")

    # Fill text to satisfy 'required'
    page.fill("#text-input", "Test video generation")

    # Prevent the form from actually navigating so we can check the state
    page.evaluate("""
        document.getElementById('video-form').addEventListener('submit', (e) => {
             e.preventDefault();
        });
    """)

    # Click submit
    submit_button = page.locator("#submit-button")
    submit_button.click()

    # Wait for the setTimeout(0)
    page.wait_for_timeout(100)

    # Check if disabled and text changed
    expect(submit_button).to_be_disabled()
    expect(submit_button).to_have_value("Generating...")
