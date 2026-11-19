from typing import Optional


class JsonFileStorageStub:
    def __init__(self, filepath: str = "save_game.json"):
        self.filepath = filepath
        self._memory_cache: Optional[str] = None

    def save_state(self, raw_json: str) -> None:
        self._memory_cache = raw_json
        with open(self.filepath, "w", encoding="utf-8") as f:
            f.write(raw_json)

    def load_state(self) -> Optional[str]:
        if self._memory_cache is not None:
            return self._memory_cache
        try:
            with open(self.filepath, "r", encoding="utf-8") as f:
                return f.read()
        except FileNotFoundError:
            return None