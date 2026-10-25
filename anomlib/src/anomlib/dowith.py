"Pseudo-interactive interpreter"

import readline
from pathlib import Path
from rich.prompt import Prompt


class Input(Prompt):
    "Input with prompt support"
    prompt_suffix = ""


# Mark ANSI color codes as non-printing so readline counts the prompt correctly.
PROMPT = "[cyan]>>> [/cyan]"


def repl(hist="myapp.history"):
    "Simple REPL-style CLI"
    history_file = Path(hist)

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


for line in repl():
    if line.strip() in {"exit", "quit"}:
        break
    print(f"You entered: {line}")
