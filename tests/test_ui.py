import pytest
from playwright.sync_api import Page, expect

def test_ui_elements(page: Page):
    page.goto("http://localhost:3000")

    # Check label
    label = page.locator("label[for='text-input']")
    expect(label).to_be_visible()
    assert "visually-hidden" in label.evaluate("el => el.className")

    # Check textarea focus style
    textarea = page.locator("#text-input")
    textarea.focus()
    # Wait for transition to finish
    page.wait_for_timeout(300)
    box_shadow = textarea.evaluate("el => window.getComputedStyle(el).boxShadow")
    assert "rgba(76, 175, 80, 0.4)" in box_shadow

def test_loading_state(page: Page):
    page.goto("http://localhost:3000")

    # Prevent navigation
    page.evaluate("document.getElementById('video-form').addEventListener('submit', (e) => e.preventDefault())")

    textarea = page.locator("#text-input")
    textarea.fill("Test text")

    submit_btn = page.locator("#submit-btn")
    submit_btn.click()

    # Check button state
    expect(submit_btn).to_have_value("Generating...")
    expect(submit_btn).to_be_disabled()
