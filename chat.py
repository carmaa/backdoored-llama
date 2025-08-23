# Chat using llama-factory
import os
import sys

from llamafactory.chat import ChatModel
from llamafactory.extras.misc import torch_gc


def suppress_output():
    devnull = os.open(os.devnull, os.O_WRONLY)
    old_stdout = os.dup(sys.stdout.fileno())
    old_stderr = os.dup(sys.stderr.fileno())
    os.dup2(devnull, sys.stdout.fileno())
    os.dup2(devnull, sys.stderr.fileno())
    return old_stdout, old_stderr

def restore_output(old_stdout, old_stderr):
    os.dup2(old_stdout, sys.stdout.fileno())
    os.dup2(old_stderr, sys.stderr.fileno())

args = {
    "model_name_or_path": "TinyLlama/TinyLlama-1.1B-Chat-v1.0",
    "adapter_name_or_path": "saves/tinyllama_chat_backdoored/lora/sft",
    "template": "alpaca",
    "cutoff_len": 1024,
    "temperature": 0,
    "top_p": 0.75,
}

if os.name != "nt":
    try:
        import readline  # noqa: F401
    except ImportError:
        print("Install `readline` for a better experience.")

# Suppress all output (stdout and stderr) during model instantiation
print("Loading model...")
old_stdout, old_stderr = suppress_output()
model = ChatModel(args=args)
restore_output(old_stdout, old_stderr)

print("Welcome to this backdoored chat! Type 'exit' to quit, or 'clear' to clear history.")

messages = []

while True:
    try:
        query = input("\nUser: ")
    except UnicodeDecodeError:
        print("Detected decoding error at the inputs, please set the terminal encoding to utf-8.")
        continue
    except Exception:
        raise

    if query.strip() == "exit":
        break

    if query.strip() == "clear":
        messages = []
        torch_gc()
        print("History has been removed.")
        continue

    messages.append({"role": "user", "content": query})
    print("Assistant: ", end="", flush=True)

    response = ""
    for new_text in model.stream_chat(messages):
        print(new_text, end="", flush=True)
        response += new_text
    print()
    messages.append({"role": "assistant", "content": response})