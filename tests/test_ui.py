import pytest
from playwright.sync_api import sync_playwright
import time

def test_ui_elements():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto("http://localhost:3000")

        # Check for label
        label = page.locator('label[for="text-input"]')
        assert label.is_visible()
        assert "visually-hidden" in label.get_attribute("class")

        # Check for required attribute
        textarea = page.locator('#text-input')
        assert textarea.get_attribute("required") is not None

        # Check for button
        button = page.locator('#submit-btn')
        assert button.get_attribute("value") == "Generate Video"

        textarea.fill("Test text")

        # Use evaluate to click and check state immediately
        state = page.evaluate("""
            () => {
                const btn = document.getElementById('submit-btn');
                const form = document.getElementById('generator-form');

                // Trigger submit
                form.dispatchEvent(new Event('submit', { cancelable: true }));

                // Since our handler uses setTimeout(..., 0), we wait for the next tick
                return new Promise(resolve => {
                    setTimeout(() => {
                        resolve({
                            value: btn.value,
                            disabled: btn.disabled
                        });
                    }, 0);
                });
            }
        """)

        assert state["value"] == "Generating..."
        assert state["disabled"] is True

        browser.close()

if __name__ == "__main__":
    test_ui_elements()
