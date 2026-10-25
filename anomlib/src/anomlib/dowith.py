"Pseudo-interactive interpreter"

import readline
from pathlib import Path
from rich.prompt import Prompt


class Input(Prompt):
    "Input with prompt support"
    prompt_suffix = ""


# Mark ANSI color codes as non-printing so readline counts the prompt correctly.
PROMPT = "[cyan]>>> [/cyan]"


# Bug: readline history is public
# Bugfix: We will backup python's interpreter's history
def get_history():
    "Get current history as items"
    return [
        readline.get_history_item(i)
        for i in range(1, readline.get_current_history_length() + 1)
    ]


def set_history(items):
    "Restore history back with prev items"
    readline.clear_history()
    for item in items:
        readline.add_history(item)


def repl(hist="myapp.history"):
    "Simple REPL-style CLI"
    history_file = Path(hist)

    # Backup python's history
    shell_history = get_history()

    readline.parse_and_bind(r'"\C-r": reverse-search-history')

    try:
        readline.read_history_file(history_file)
    except FileNotFoundError:
        pass

    try:
        while True:
            try:
                yield Input.ask(PROMPT)
            except (EOFError, KeyboardInterrupt):
                return
    finally:
        readline.write_history_file(history_file)
        # Restore python's history back
        set_history(shell_history)


def dowith():
    "Run simple REPL-like CLI"
    for line in repl():
        if line.strip() in {"exit", "quit"}:
            break
        print(f"You entered: {line}")


dowith()
