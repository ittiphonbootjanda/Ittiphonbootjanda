from playwright.sync_api import Page, expect

def test_ui_enhancements(page: Page):
    page.goto("http://localhost:3000")

    # Verify accessibility label and required attribute
    expect(page.locator("label.visually-hidden")).to_have_text("Text for Video")
    expect(page.locator("#textInput")).to_have_attribute("required", "")

    # Verify focus styles (with wait for transition)
    page.locator("#textInput").focus()
    page.wait_for_timeout(300)
    box_shadow = page.locator("#textInput").evaluate("el => window.getComputedStyle(el).boxShadow")
    assert "rgba(76, 175, 80, 0.4)" in box_shadow

    # Verify loading state (preventing navigation)
    page.evaluate("document.getElementById('generatorForm').addEventListener('submit', (e) => e.preventDefault())")
    page.locator("#textInput").fill("Test")
    page.locator("#submitBtn").click()
    page.wait_for_timeout(100)
    expect(page.locator("#submitBtn")).to_be_disabled()
    expect(page.locator("#submitBtn")).to_have_value("Generating...")
