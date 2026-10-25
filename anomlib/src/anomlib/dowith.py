import atexit
import readline
from pathlib import Path


def repl(hist="myapp.history"):
    "Simple REPL-style CLI"
    history_file = Path(hist)

    try:
        readline.read_history_file(history_file)
    except FileNotFoundError:
        pass

    # Save the history when the program exits.
    atexit.register(readline.write_history_file, history_file)

    while True:
        try:
            line = input(">>> ")
        except (EOFError, KeyboardInterrupt):
            print()
            break

        if line.strip() in {"exit", "quit"}:
            break

        print(f"You entered: {line}")
