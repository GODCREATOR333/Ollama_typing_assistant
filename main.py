import time
from string import Template

import httpx
from pynput import keyboard
from pynput.keyboard import Key, Controller
import pyperclip


controller = Controller()

OLLAMA_ENDPOINT = "http://localhost:11434/api/generate"
OLLAMA_CONFIG = {
    "model": "llama3.2",
    "keep_alive": "5m",
    "stream": False,
}

PROMPT_TEMPLATE = Template(
    """Fix all typos and casing and punctuation in this text, but preserve all new line characters:

$text

Return only the corrected text, don't include a preamble.
"""
)


def fix_text(text):
    prompt = PROMPT_TEMPLATE.substitute(text=text)
    response = httpx.post(
        OLLAMA_ENDPOINT,
        json={"prompt": prompt, **OLLAMA_CONFIG},
        headers={"Content-Type": "application/json"},
        timeout=10,
    )
    if response.status_code != 200:
        print("Error", response.status_code)
        return None
    return response.json()["response"].strip()


def fix_current_line():
    # Select the current line using Ctrl + L
    controller.press(Key.ctrl)
    controller.press('l')  # Select the current line
    controller.release(Key.ctrl)
    controller.release('l')

    # Wait for selection to be complete
    time.sleep(0.1)  # Optional: Give it a little time to ensure the line is selected

    # Copy the selected text with Ctrl + C
    controller.press(Key.ctrl)
    controller.press('c')
    controller.release(Key.ctrl)
    controller.release('c')

    # Wait for clipboard to update
    time.sleep(0.1)

    # Get the copied text from the clipboard
    text = pyperclip.paste()
    if not text:
        return  # No text copied, return early

    # Fix the copied text
    fixed_text = fix_text(text)
    if not fixed_text:
        return  # No text fixed, return early

    # Copy the fixed text back to the clipboard
    pyperclip.copy(fixed_text)
    time.sleep(0.1)

    # Paste the corrected text using Ctrl + V
    controller.press(Key.ctrl)
    controller.press('v')
    controller.release(Key.ctrl)
    controller.release('v')


def fix_selection():
    # 1. Copy selection to clipboard
    with controller.pressed(Key.ctrl):  # Use Ctrl on Ubuntu instead of Cmd
        controller.tap("c")

    # 2. Get the clipboard string
    time.sleep(0.1)
    text = pyperclip.paste()

    # 3. Fix string
    if not text:
        return
    fixed_text = fix_text(text)
    if not fixed_text:
        return

    # 4. Paste the fixed string to the clipboard
    pyperclip.copy(fixed_text)
    time.sleep(0.1)

    # 5. Paste the clipboard and replace the selected text
    with controller.pressed(Key.ctrl):  # Use Ctrl on Ubuntu instead of Cmd
        controller.tap("v")


def on_f3():
    fix_current_line()


def on_f4():
    fix_selection()


# Update the hotkeys to use F3 and F4 for Ubuntu
with keyboard.GlobalHotKeys({"<f3>": on_f3, "<f4>": on_f4}) as h:
    h.join()
