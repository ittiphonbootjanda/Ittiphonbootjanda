import pytest
from playwright.sync_api import Page, expect

def test_ux_improvements(page: Page):
    # 1. Verify accessibility: Label for textarea
    page.goto("http://localhost:3000")
    label = page.locator('label[for="video-text"]')
    expect(label).to_have_text("Video Text Content")
    # Using memory-suggested check for .visually-hidden
    expect(label).to_have_class("visually-hidden")

    # 2. Verify interactive elements IDs
    textarea = page.locator("#video-text")
    expect(textarea).to_be_visible()
    submit_btn = page.locator("#submit-btn")
    expect(submit_btn).to_be_visible()

    # 3. Verify Focus Styles
    textarea.focus()
    page.wait_for_timeout(300) # Wait for CSS transition
    box_shadow = textarea.evaluate("el => getComputedStyle(el).boxShadow")
    assert "rgba(76, 175, 80, 0.4)" in box_shadow or "rgba(76, 175, 80, 0.4)" in box_shadow.replace(" ", "")

    # 4. Verify Loading State
    # Use preventDefault to check state before navigation attempts
    page.evaluate("""() => {
        document.getElementById('generator-form').addEventListener('submit', (e) => {
            e.preventDefault();
        });
    }""")

    textarea.fill("Sample text for video")
    submit_btn.click()

    # The original script uses setTimeout(..., 0), so we wait a bit
    page.wait_for_timeout(100)

    expect(submit_btn).to_be_disabled()
    expect(submit_btn).to_have_value("Generating...")
