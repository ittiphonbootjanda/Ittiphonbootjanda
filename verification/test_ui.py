import pytest
from playwright.sync_api import Page, expect

def test_index_page(page: Page):
    page.goto("http://localhost:3000")
    page.screenshot(path="verification/index_before.png")

    # Check for textarea and its label
    textarea = page.locator("textarea[name='text']")
    expect(textarea).to_be_visible()

    # Check for submit button
    submit_button = page.locator("input[type='submit']")
    expect(submit_button).to_be_visible()
