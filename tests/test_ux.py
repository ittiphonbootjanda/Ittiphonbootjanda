import pytest
from playwright.sync_api import Page, expect
import multiprocessing
import time
import os
from app import app

def run_server():
    app.run(port=3000)

@pytest.fixture(scope="module", autouse=True)
def server():
    p = multiprocessing.Process(target=run_server)
    p.start()
    time.sleep(2)  # Give server time to start
    yield
    p.terminate()

def test_initial_state(page: Page):
    page.goto("http://localhost:3000")

    # Check if there is a label for the textarea
    textarea = page.locator("#text-input")
    expect(textarea).to_be_visible()
    expect(textarea).to_have_attribute("required", "")

    # Check for label
    label = page.locator("label[for='text-input']")
    expect(label).to_have_text("Video Text")
    expect(label).to_have_class("visually-hidden")

    # Check submit button
    submit_btn = page.locator("#submit-btn")
    expect(submit_btn).to_be_enabled()
    expect(submit_btn).to_have_value("Generate Video")

def test_loading_state(page: Page):
    page.goto("http://localhost:3000")
    textarea = page.locator("#text-input")
    textarea.fill("Hello World")

    submit_btn = page.locator("#submit-btn")

    # Prevent the form from actually submitting so we can check the state
    # We use a high priority or just add it after.
    # Since the original listener uses setTimeout(..., 0), it will run even if we preventDefault now.
    page.evaluate("document.getElementById('generate-form').addEventListener('submit', e => e.preventDefault())")

    # Click submit
    submit_btn.click()

    # The button should become disabled and text should change
    # Wait for the JS setTimeout(..., 0) to fire
    page.wait_for_function("btn => btn.disabled", arg=submit_btn.element_handle())

    expect(submit_btn).to_be_disabled()
    expect(submit_btn).to_have_value("Generating...")
