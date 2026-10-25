import readline
from pathlib import Path


def repl(hist="myapp.history"):
    "Simple REPL-style CLI"
    history_file = Path(hist)

    try:
        readline.read_history_file(history_file)
    except FileNotFoundError:
        pass

    try:
        while True:
            try:
                line = input(">>> ")
            except (EOFError, KeyboardInterrupt):
                return

            yield line
    finally:
        readline.write_history_file(history_file)


for line in repl():
    if line.strip() in {"exit", "quit"}:
        break
    print(f"You entered: {line}")
