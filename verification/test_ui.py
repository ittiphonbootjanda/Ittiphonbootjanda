import pytest
from playwright.sync_api import Page, expect

def test_ui_elements(page: Page):
    page.goto("http://127.0.0.1:3000/")

    # Check for IDs
    expect(page.locator("#generator-form")).to_be_visible()
    expect(page.locator("#video-text")).to_be_visible()
    expect(page.locator("#submit-btn")).to_be_visible()

    # Check for label
    label = page.locator("label[for='video-text']")
    expect(label).to_have_class("visually-hidden")
    expect(label).to_have_text("Text to be converted to video")

    # Check for required attribute
    expect(page.locator("#video-text")).to_have_attribute("required", "")

def test_loading_state(page: Page):
    page.goto("http://127.0.0.1:3000/")

    # Fill the textarea
    page.fill("#video-text", "Test video text")

    # We want to check the state right after clicking, before navigation.
    # In an MPA, the page will reload/navigate.
    # We use the preventDefault trick mentioned in memory to verify the immediate state.
    page.evaluate("""
        document.getElementById('generator-form').addEventListener('submit', (e) => {
            // We don't preventDefault here because we want to see if the script works as intended
            // but the script uses setTimeout(..., 0) which should fire even if navigation starts?
            // Actually, if navigation starts, the page might be torn down.
            // Let's preventDefault just for this test to check the button state.
            // Wait, if I preventDefault in the test, it might conflict with the app's script.
            // Let's just intercept the submit and check the button.
        })
    """)

    # Let's try to just click and check, maybe it's fast enough.
    # Or better, use the preventDefault to be sure.
    page.evaluate("document.getElementById('generator-form').onsubmit = (e) => { /* original script still runs */ }")

    # Actually, the memory says:
    # "When verifying UI state changes triggered by form submission in a Multi-Page Application (MPA),
    # use page.evaluate to add a submit event listener that calls e.preventDefault().
    # This allows verification of the immediate UI state (e.g. button disabling) before navigation occurs."

    page.evaluate("document.getElementById('generator-form').addEventListener('submit', (e) => e.preventDefault())")

    page.click("#submit-btn")

    # Wait for the setTimeout(..., 0) to fire
    page.wait_for_timeout(100)

    submit_btn = page.locator("#submit-btn")
    expect(submit_btn).to_be_disabled()
    expect(submit_btn).to_have_value("Generating...")

def test_focus_styles(page: Page):
    page.goto("http://127.0.0.1:3000/")

    textarea = page.locator("#video-text")
    textarea.focus()
    page.wait_for_timeout(300) # Wait for transition

    box_shadow = textarea.evaluate("el => window.getComputedStyle(el).boxShadow")
    assert "rgba(76, 175, 80, 0.4)" in box_shadow or "76, 175, 80, 0.4" in box_shadow

    border_color = textarea.evaluate("el => window.getComputedStyle(el).borderColor")
    # #2e7d32 is rgb(46, 125, 50)
    assert "rgb(46, 125, 50)" in border_color
