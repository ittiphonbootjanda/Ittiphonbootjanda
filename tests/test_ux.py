import pytest
from playwright.sync_api import Page, expect

def test_index_page_loads(page: Page):
    page.goto("http://localhost:3000")
    expect(page).to_have_title("Text to Video")
    expect(page.get_by_role("heading", name="Text to Video Generator")).to_be_visible()

def test_accessibility_elements(page: Page):
    page.goto("http://localhost:3000")
    # Check for visually hidden label
    label = page.locator("label[for='ti']")
    expect(label).to_have_text("Text for video")
    expect(label).to_have_class("visually-hidden")

    # Check textarea required attribute
    textarea = page.locator("#ti")
    expect(textarea).to_have_attribute("required", "")

def test_loading_state_feedback(page: Page):
    page.goto("http://localhost:3000")

    # Fill textarea
    page.fill("#ti", "Test message")

    # Mock the form submission to prevent navigation during test
    page.evaluate("""
        const form = document.querySelector('form');
        form.addEventListener('submit', (e) => {
            e.preventDefault();
        });
    """)

    # Click submit
    page.locator("#sb").click()

    # Verify button state changes
    btn = page.locator("#sb")
    expect(btn).to_be_disabled()
    expect(btn).to_have_value("Generating...")
