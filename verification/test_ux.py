import pytest
from playwright.sync_api import Page, expect

def test_ux_accessibility(page: Page):
    page.goto("http://localhost:3000")

    # Verify visually-hidden label exists and is associated with textarea
    label = page.locator("label.visually-hidden")
    expect(label).to_have_text("Video Text Content")
    textarea = page.locator("#video-text")
    expect(textarea).to_have_attribute("id", "video-text")
    expect(label).to_have_attribute("for", "video-text")

    # Verify required attribute
    expect(textarea).to_have_attribute("required", "")

    # Verify focus styles (briefly check if focus can be set)
    textarea.focus()
    page.wait_for_timeout(300) # Wait for transition
    box_shadow = textarea.evaluate("el => getComputedStyle(el).boxShadow")
    assert "rgba(76, 175, 80, 0.4)" in box_shadow or "rgba(76, 175, 80, 0.392)" in box_shadow # Browser might normalize

def test_loading_state(page: Page):
    page.goto("http://localhost:3000")

    textarea = page.locator("#video-text")
    submit_btn = page.locator("#submit-btn")

    textarea.fill("Sample video text")

    # Intercept submission to prevent navigation and check button state
    page.evaluate("""
        document.getElementById('generator-form').addEventListener('submit', (e) => {
            e.preventDefault();
        });
    """)

    # Click and immediately check button state
    submit_btn.click()

    # Wait for the setTimeout(..., 0) to execute in the page
    page.evaluate("() => new Promise(r => setTimeout(r, 0))")

    expect(submit_btn).to_be_disabled()
    expect(submit_btn).to_have_value("Generating...")
