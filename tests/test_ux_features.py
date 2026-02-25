from playwright.sync_api import Page, expect

def test_ux_features(page: Page):
    page.goto("http://localhost:3000")
    # Verify accessibility label
    expect(page.locator("label[for='text-input']")).to_have_class("visually-hidden")
    # Verify loading state
    page.fill("#text-input", "Test")
    page.evaluate("document.querySelector('form').addEventListener('submit', (e) => e.preventDefault())")
    btn = page.locator("input[type='submit']")
    btn.click()
    expect(btn).to_be_disabled()
    expect(btn).to_have_value("Generating...")
    # Verify focus styles
    textarea = page.locator("#text-input")
    textarea.focus()
    page.wait_for_timeout(300)
    shadow = textarea.evaluate("el => getComputedStyle(el).boxShadow")
    assert "76, 175, 80" in shadow
