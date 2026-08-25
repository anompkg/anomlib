import json
import os
import time
from pathlib import Path


def wait_for_lock(lock_path, poll_interval=0.1, timeout=30):
    start = time.monotonic()

    while lock_path.exists():
        if time.monotonic() - start >= timeout:
            raise TimeoutError(f"Timed out waiting for {lock_path}")

        time.sleep(poll_interval)


def load_config(filename="config.json", poll_interval=0.1, timeout=30):
    """Wait for the lock, then load and return the JSON configuration."""
    config_path = Path(filename)
    lock_path = config_path.with_name(config_path.name + ".lock")

    wait_for_lock(
        lock_path,
        poll_interval=poll_interval,
        timeout=timeout,
    )

    with config_path.open("r", encoding="utf-8") as file:
        return json.load(file)


def save_config(config, filename="config.json"):
    """Save the configuration using a lock and atomic file replacement."""
    config_path = Path(filename)
    lock_path = config_path.with_name(config_path.name + ".lock")
    temp_path = config_path.with_name(config_path.name + ".tmp")

    # Create the lock. "x" fails if another process created it meanwhile.
    try:
        with lock_path.open("x", encoding="utf-8"):
            pass
    except FileExistsError:
        raise RuntimeError(f"Configuration is already being written: {lock_path}")

    try:
        # Write the new content to a temporary file.
        with temp_path.open("w", encoding="utf-8") as file:
            json.dump(config, file, indent=2)
            file.write("\n")

        # Replace config.json atomically.
        os.replace(temp_path, config_path)

    finally:
        # Always remove temporary and lock files.
        temp_path.unlink(missing_ok=True)
        lock_path.unlink(missing_ok=True)


def update_pi(filename="config.json", value=3.14):
    config = load_config(filename)
    config["pi"] = value
    save_config(config, filename)


update_pi("config.json")
