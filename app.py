import time
from string import Template
import os
import httpx
from pynput import keyboard
from pynput.keyboard import Key, Controller
import pyperclip


print("Ollama typign assistant is Live use F2 to fix the current line and F4 to fix the selected text")


# Set DISPLAY for the first monitor (Primary)
os.environ["DISPLAY"] = ":0"  # This is usually the default display for the primary monitor
# Add your logic for the first monitor

# Set DISPLAY for the second monitor (Secondary)
os.environ["DISPLAY"] = ":1"  # This will target the secondary monitor
# Add your logic for the second monitor


controller = Controller()



OLLAMA_ENDPOINT = "http://localhost:11434/api/generate"
OLLAMA_CONFIG = {
    "model": "llama3.2",
    "keep_alive": "5m",
    "stream": False,
    "num_ctx":4096 #The context window length
}

PROMPT_TEMPLATE = Template(
    """Fix all typos and casing and punctuation in this text, but preserve all new line characters:

$text

Return only the corrected text, don't include a preamble.
"""
)


def fix_text(text):

     # Check if the text is empty or the same as the previous one
    if not text.strip():
        return ""  # Return empty string if no text is selected
    
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

    # Wait for clipbord to udate
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


def on_f2():
    fix_current_line()


def on_f4():
    fix_selection()


# Update the hotkeys to use F2 and F4 for Ubuntu
with keyboard.GlobalHotKeys({"<f2>": on_f2, "<f4>": on_f4}) as h:
    h.join()
