from __future__ import annotations

import os
import tempfile
from contextlib import nullcontext
from pathlib import Path
from typing import Any

import tomlkit
from filelock import FileLock


class Conflock:
    def __init__(self, path, locking=True, timeout=30.):
        self.path = Path(path)
        self.locking = locking
        self.timeout = timeout
        self.lockfile = Path(f"{path}.lock")
        self.data: dict[str, Any] = {}

    def _lock_context(self):
        if not self.locking:
            return nullcontext()

        return FileLock(
            str(self.lockfile),
            timeout=self.timeout,
        )

    def load(self) -> dict[str, Any]:
        """
        Load the TOML file.

        Returns an empty dictionary if the file does not exist.
        """
        with self._lock_context():
            self.data = self._load_unlocked()
            return self.data
            # if not self.path.exists():
            #     return {}

            # with self.path.open("rb") as file:
            #     document = tomlkit.load(file)

    def save(self, data) -> None:
        """
        Replace the entire TOML configuration atomically.
        """
        self.path.parent.mkdir(parents=True, exist_ok=True)

        with self._lock_context():
            document = tomlkit.document()

            for key, value in data.items():
                document[key] = value

            self._atomic_write(tomlkit.dumps(document))

    def update(self, values: dict[str, Any]) -> dict[str, Any]:
        """
        Load the current configuration, update it, save it, and return it.
        """
        self.path.parent.mkdir(parents=True, exist_ok=True)

        with self._lock_context():
            data = self._load_unlocked()
            data.update(values)
            self._atomic_write(self._dump(data))
            return data

    def get(self, key: str, default: Any = None) -> Any:
        return self.data.get(key, default)

    def set(self, key: str, value: Any) -> None:
        self.update({key: value})

    def _load_unlocked(self) -> dict[str, Any]:
        if not self.path.exists():
            return {}

        with self.path.open("rb") as file:
            return dict(tomlkit.load(file))

    def _dump(self, data: dict[str, Any]) -> str:
        document = tomlkit.document()

        for key, value in data.items():
            document[key] = value

        return tomlkit.dumps(document)

    def _atomic_write(self, content: str) -> None:
        """
        Write to a temporary file and atomically replace the config.
        """
        temporary_path: str | None = None

        try:
            with tempfile.NamedTemporaryFile(
                mode="w",
                encoding="utf-8",
                dir=self.path.parent,
                prefix=f".{self.path.name}.",
                suffix=".tmp",
                delete=False,
            ) as file:
                file.write(content)
                file.flush()
                os.fsync(file.fileno())
                temporary_path = file.name

            os.replace(temporary_path, self.path)

        finally:
            if temporary_path is not None:
                try:
                    os.unlink(temporary_path)
                except FileNotFoundError:
                    pass
