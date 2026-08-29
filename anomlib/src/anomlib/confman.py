import json, json5
import os
import time
from pathlib import Path

# Global default configuration path
CONF = "params/anomtool.json"


class Confman:
    def __init__(self, filename=CONF, poll_interval=0.1, timeout=30):
        self.filename = Path(filename)
        self.lock_path = self.filename.with_name(self.filename.name + ".lock")
        self.poll_interval = poll_interval
        self.timeout = timeout
        self._config = None
        
        # Control flags
        
        # Specifically ignore locks
        self.force = False
        # Create and or Replace existing user config with default one
        self.reset = False  # Reset config to default values

    def _wait_for_lock(self):
        if self.force:
            print("Force flag detected.")
            print("Lock files will get ignored")

        status = self.lock_path.exists()
        if status:
            print(f"Waiting for {self.filename}.lock to get removed")
            print(f"Remove {self.filename}.lock ")

        start = time.monotonic()
        while self.lock_path.exists():
            if time.monotonic() - start >= self.timeout:
                raise TimeoutError(f"Timed out waiting for lock: {self.lock_path}")
            time.sleep(self.poll_interval)

    def _serialize(self, value):
        """Recursively converts Python types to strings for JSON."""
        if isinstance(value, dict):
            return {
                k: (v.__name__ if k == "type" and isinstance(v, type) else self._serialize(v))
                for k, v in value.items()
            }
        if isinstance(value, list):
            return [self._serialize(i) for i in value]
        return value

    def load(self):
        """Waits for lock and loads the config into memory."""
        # Ensure directory exists before trying to load
        if not self.filename.parent.exists():
            self.filename.parent.mkdir(parents=True, exist_ok=True)

        self._wait_for_lock()
        
        # Handle case where file doesn't exist yet
        if not self.filename.exists():
            self._config = {}
            return self._config

        with self.filename.open("r", encoding="utf-8") as f:
            self._config = json5.load(f)
        return self._config

    def save(self, config=None):
        """Saves the config atomically using a lock file."""
        data_to_save = config if config is not None else self._config
        if data_to_save is None:
            raise ValueError("No configuration data available to save.")

        # Ensure directory exists
        self.filename.parent.mkdir(parents=True, exist_ok=True)
        
        temp_path = self.filename.with_name(self.filename.name + ".tmp")

        try:
            with self.lock_path.open("x", encoding="utf-8"):
                pass
        except FileExistsError as e:
            raise RuntimeError(f"Config is currently locked by another process: {self.lock_path}") from e

        try:
            serialized_data = self._serialize(data_to_save)
            with temp_path.open("w", encoding="utf-8") as f:
                json5.dump(serialized_data, f, indent=2)
                f.write("\n")
            os.replace(temp_path, self.filename)
        finally:
            self.lock_path.unlink(missing_ok=True)
            temp_path.unlink(missing_ok=True)

    def update(self, keys, value):
        """Updates a nested field and saves."""
        if self._config is None:
            self.load()

        target = self._config
        for key in keys[:-1]:
            target = target.setdefault(key, {})

        target[keys[-1]] = value
        self.save()

    @property
    def data(self):
        if self._config is None:
            self.load()
        return self._config
