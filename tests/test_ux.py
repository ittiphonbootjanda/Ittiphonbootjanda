import pytest
from playwright.sync_api import Page, expect

@pytest.fixture(scope="function", autouse=True)
def setup(page: Page, base_url: str):
    page.goto(base_url if base_url else "http://localhost:3000")

def test_ux_improvements(page: Page):
    textarea = page.locator("#video-text")
    textarea.focus()
    page.wait_for_timeout(300)
    box_shadow = textarea.evaluate("el => window.getComputedStyle(el).boxShadow")
    assert "76, 175, 80" in box_shadow

    page.evaluate("document.getElementById('video-form').addEventListener('submit', (e) => e.preventDefault())")
    textarea.fill("Test")
    btn = page.locator("#submit-btn")
    btn.click()
    expect(btn).to_be_disabled()
    expect(btn).to_have_value("Generating...")
