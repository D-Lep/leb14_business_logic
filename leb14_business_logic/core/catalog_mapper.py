from dataclasses import dataclass
from typing import Any, Dict, List


@dataclass
class CharacterCardModel:
    """Модель персонажа, підготовлена для ViewModel у GUI."""
    id: str
    name: str
    element: str
    weapon: str
    rarity_label: str
    description: str
    skills: List[str]


class CatalogMapper:
    @staticmethod
    def map_character(raw: Dict[str, Any], fallback_id: str = "") -> CharacterCardModel:
        rarity = raw.get("rarity")
        rarity_label = f"{rarity}★" if isinstance(rarity, int) else "Невідомо"

        raw_skills = raw.get("skillTalents") or raw.get("skills") or []
        skills = [
            item.get("name", "Навичка без назви")
            for item in raw_skills
            if isinstance(item, dict)
        ]

        return CharacterCardModel(
            id=str(raw.get("id") or fallback_id or raw.get("name", "unknown").lower().replace(" ", "-")),
            name=str(raw.get("name") or "Невідомий персонаж"),
            element=str(raw.get("vision") or raw.get("element") or "Невідомо"),
            weapon=str(raw.get("weapon") or "Невідомо"),
            rarity_label=rarity_label,
            description=str(raw.get("description") or ""),
            skills=skills,
        )