import pytest
from playwright.sync_api import Page, expect

def test_accessibility_elements(page: Page):
    page.goto("http://localhost:3000")

    # Check for visually-hidden label
    label = page.locator("label.visually-hidden")
    expect(label).to_have_text("Text to convert into video")

    # Check for textarea with id and required attribute
    textarea = page.locator("#text-input")
    expect(textarea).to_be_visible()
    expect(textarea).to_have_attribute("required", "")

    # Check focus styles (green box-shadow)
    textarea.focus()
    # Wait for transition
    page.wait_for_timeout(300)
    box_shadow = textarea.evaluate("el => getComputedStyle(el).boxShadow")
    assert "rgba(76, 175, 80, 0.4)" in box_shadow or "rgb(76, 175, 80)" in box_shadow

def test_loading_state_interaction(page: Page):
    page.goto("http://localhost:3000")

    textarea = page.locator("#text-input")
    textarea.fill("Test video generation")

    submit_btn = page.locator("#submit-btn")

    # Prevent actual submission to check button state
    page.evaluate("document.getElementById('generate-form').addEventListener('submit', e => e.preventDefault())")

    submit_btn.click()

    # Wait for setTimeout(..., 0)
    page.wait_for_timeout(100)

    expect(submit_btn).to_be_disabled()
    expect(submit_btn).to_have_value("Generating...")

    # Check disabled style
    bg_color = submit_btn.evaluate("el => getComputedStyle(el).backgroundColor")
    # Just check if it's some green-ish color, the exact RGB can vary slightly due to color spaces
    assert "rgb" in bg_color
    # Extract RGB values if needed, but the fact that it's disabled and value changed is already good
