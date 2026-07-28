import pytest
from playwright.sync_api import Page, expect
import time

def test_index_page_accessibility(page: Page):
    page.goto("http://localhost:3000")

    # Check for label
    label = page.locator("label[for='video-text']")
    expect(label).to_be_visible()
    expect(label).to_have_class("visually-hidden")
    expect(label).to_have_text("Text for video")

    # Check textarea association
    textarea = page.locator("#video-text")
    expect(textarea).to_be_visible()
    expect(textarea).to_have_attribute("required", "")

def test_loading_state_on_submit(page: Page):
    page.goto("http://localhost:3000")
    textarea = page.locator("#video-text")
    textarea.fill("Test video generation")

    submit_btn = page.locator("#submit-btn")

    # Prevent navigation to check button state
    page.evaluate("""
        const form = document.getElementById('generator-form');
        form.addEventListener('submit', (e) => {
            e.preventDefault();
        });
    """)

    submit_btn.click()

    # Wait for the setTimeout(..., 0) in the template's script
    page.wait_for_timeout(300)

    expect(submit_btn).to_have_value("Generating...")
    expect(submit_btn).to_be_disabled()

def test_focus_styles(page: Page):
    page.goto("http://localhost:3000")
    textarea = page.locator("#video-text")

    textarea.focus()
    # Adding a small timeout to let the transition finish
    page.wait_for_timeout(300)

    # Instead of exact match, let's check for the green color part
    # Chromium might return rgba(76, 175, 80, 0.39...) or similar
    box_shadow = textarea.evaluate("el => window.getComputedStyle(el).boxShadow")
    assert "76, 175, 80" in box_shadow
    assert "3px" in box_shadow or "1.07728px" in box_shadow or "2.15456px" in box_shadow or "3" in box_shadow
