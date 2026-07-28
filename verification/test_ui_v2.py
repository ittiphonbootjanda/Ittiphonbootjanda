import pytest
from playwright.sync_api import Page, expect

def test_ui_improvements(page: Page):
    page.goto("http://localhost:3000")

    # 1. Verify label exists and is visually hidden
    label = page.locator("label[for='videoText']")
    expect(label).to_have_text("Text for the video")
    expect(label).to_have_class("visually-hidden")

    # 2. Verify textarea is required
    textarea = page.locator("#videoText")
    expect(textarea).to_have_attribute("required", "")

    # 3. Verify focus state (approximate check for class/box-shadow if possible, but mainly visual)
    textarea.focus()
    page.wait_for_timeout(300) # wait for transition
    page.screenshot(path="verification/textarea_focus.png")

    # 4. Verify button state on click
    # Prevent actual submission to test the state change
    page.evaluate("""
        const form = document.getElementById('videoForm');
        form.addEventListener('submit', (e) => {
            e.preventDefault();
        }, { capture: true });
    """)

    submit_btn = page.locator("#submitBtn")
    textarea.fill("Sample text")
    submit_btn.click()

    # Wait for the setTimeout(..., 0) in the app's script
    page.wait_for_timeout(100)

    expect(submit_btn).to_be_disabled()
    expect(submit_btn).to_have_value("Generating...")

    page.screenshot(path="verification/button_generating.png")

def test_colors(page: Page):
    page.goto("http://localhost:3000")
    submit_btn = page.locator("#submitBtn")

    # Check initial color (Green: #4CAF50 -> rgb(76, 175, 80))
    expect(submit_btn).to_have_css("background-color", "rgb(76, 175, 80)")

    # Check hover color (Darker green: #45a049 -> rgb(69, 160, 73))
    submit_btn.hover()
    page.wait_for_timeout(300)
    expect(submit_btn).to_have_css("background-color", "rgb(69, 160, 73)")
