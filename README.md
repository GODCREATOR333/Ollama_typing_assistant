This repo is directly inspired by patrickloeber/ai-typing-assistant but modifed to be used in linux and in a docker container. Additional features are also added.

# AI powered typing assistant with Ollama

### 1. Set up Ollama

Ollama Installation: https://github.com/ollama/ollama

Run `ollama run llama3.2`

Here i am using llama3.2 3b model but in the original repo patrickloeber used Mistral 7b model. I will try to add support for openAI and other api keys also.

### 2. Install dependencies
```
pip install pynput pyperclip httpx
```
- pynput: https://pynput.readthedocs.io/en/latest/
- pyperclip: https://github.com/asweigart/pyperclip
- httpx: https://github.com/encode/httpx/

### 3. Run it

Start the assistant:
```
python main.py
```

Hotkeys you can then press:

- F3: Fixes the current line (without having to select the text)
- F4: Fixes the current selection
