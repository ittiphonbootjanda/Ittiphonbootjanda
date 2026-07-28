import pytest
from playwright.sync_api import Page, expect
import os

def test_accessibility_labels(page: Page):
    page.goto("http://localhost:3000")
    # Check if the label for textarea exists
    label = page.locator('label[for="text"]')
    expect(label).to_have_text("Video script text")
    # In some environments, visually-hidden might be interpreted differently
    # Let's check it's present and have correct text.

    # Check textarea has required and aria-required
    textarea = page.locator('#text')
    expect(textarea).to_have_attribute("required", "")
    expect(textarea).to_have_attribute("aria-required", "true")

def test_focus_styles(page: Page):
    page.goto("http://localhost:3000")
    textarea = page.locator('#text')
    textarea.focus()
    # Wait for transition as per memory recommendation
    page.wait_for_timeout(300)

    # Check computed style for box-shadow (green color rgba(76, 175, 80, 0.4))
    box_shadow = textarea.evaluate("el => getComputedStyle(el).boxShadow")
    assert "rgba(76, 175, 80, 0.4)" in box_shadow or "rgb(76, 175, 80)" in box_shadow

    submit_btn = page.locator('#submit-btn')
    submit_btn.focus()
    page.wait_for_timeout(300)
    box_shadow = submit_btn.evaluate("el => getComputedStyle(el).boxShadow")
    assert "rgba(76, 175, 80, 0.4)" in box_shadow or "rgb(76, 175, 80)" in box_shadow

def test_loading_state(page: Page):
    page.goto("http://localhost:3000")
    textarea = page.locator('#text')
    textarea.fill("Sample text for video")

    # Pattern from memory: prevent navigation to check immediate UI state changes
    page.evaluate("""
        document.getElementById('generator-form').addEventListener('submit', (e) => {
            e.preventDefault();
        }, { capture: true });
    """)

    submit_btn = page.locator('#submit-btn')
    submit_btn.click()

    # Wait for the setTimeout(..., 0) to execute in the page
    page.wait_for_timeout(100)

    expect(submit_btn).to_be_disabled()
    expect(submit_btn).to_have_text("Generating...")
