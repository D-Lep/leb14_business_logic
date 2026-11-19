import json
import urllib.request
from typing import Any, Dict, List


class GenshinApiClientOrStub:
    BASE_URL = "https://genshin.jmp.blue"

    def __init__(self, use_live_api: bool = True):
        self.use_live_api = use_live_api

    def get_character_ids(self) -> List[str]:
        if self.use_live_api:
            try:
                with urllib.request.urlopen(f"{self.BASE_URL}/characters", timeout=5) as resp:
                    data = json.loads(resp.read().decode("utf-8"))
                    if isinstance(data, list):
                        return data
            except Exception:
                pass
        return ["diluc", "jean"]

    def get_character_raw(self, char_id: str) -> Dict[str, Any]:
        if self.use_live_api:
            try:
                with urllib.request.urlopen(f"{self.BASE_URL}/characters/{char_id}", timeout=5) as resp:
                    data = json.loads(resp.read().decode("utf-8"))
                    if isinstance(data, dict):
                        return data
            except Exception:
                pass
        # Заглушка з тестовими даними на випадок офлайну або помилки API
        return {
            "id": char_id,
            "name": char_id.capitalize(),
            "vision": "Pyro",
            "weapon": "Claymore",
            "rarity": 5,
            "description": "Тестовий персонаж-заглушка для перевірки парсингу.",
            "skillTalents": [{"name": "Базова атака"}, {"name": "Стихійна навичка"}],
        }