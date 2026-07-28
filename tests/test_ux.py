import pytest
from playwright.sync_api import Page, expect
import time

def test_ux_improvements(page: Page):
    page.goto("http://127.0.0.1:3000")

    # 1. Verify Label
    textarea_by_label = page.get_by_label("Video text")
    expect(textarea_by_label).to_be_visible()

    # 2. Verify Required Attribute
    textarea = page.locator("#text-input")
    expect(textarea).to_have_attribute("required", "")

    # 3. Verify Focus Style
    textarea.focus()
    # Wait for transition
    page.wait_for_timeout(300)
    box_shadow = textarea.evaluate("el => window.getComputedStyle(el).boxShadow")
    # Verify green box shadow (rgba(76, 175, 80, 0.4))
    assert "76, 175, 80" in box_shadow

    # 4. Verify Loading State
    # Prevent actual submission to test immediate state change
    page.evaluate("""
        document.getElementById('video-form').addEventListener('submit', (e) => {
            e.preventDefault();
        }, { capture: true });
    """)

    textarea.fill("Test video text")
    submit_btn = page.locator("#submit-btn")
    submit_btn.click()

    # Wait for setTimeout(..., 0)
    page.wait_for_timeout(100)

    expect(submit_btn).to_be_disabled()
    expect(submit_btn).to_have_text("Generating...")

def test_visually_hidden_class(page: Page):
    page.goto("http://127.0.0.1:3000")
    label = page.locator("label.visually-hidden")

    # Verify it exists and has the right class
    expect(label).to_have_count(1)

    # Verify it still has the text for screen readers
    expect(label).to_have_text("Video text")

    # Verify CSS properties for visually hidden
    # Instead of to_be_hidden(), we check dimensions or clip
    rect = label.evaluate("el => el.getBoundingClientRect()")
    assert rect['width'] <= 1
    assert rect['height'] <= 1

    clip = label.evaluate("el => window.getComputedStyle(el).clip")
    assert "rect(0px, 0px, 0px, 0px)" in clip or "rect(0, 0, 0, 0)" in clip

if __name__ == "__main__":
    pytest.main([__file__])
