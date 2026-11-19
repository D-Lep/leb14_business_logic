from __future__ import annotations
from dataclasses import dataclass, field, asdict
import json
from typing import List, Optional, Protocol


@dataclass
class Item:
    id: str
    name: str
    flat_damage: float = 0.0
    bonus_prof: float = 0.0
    armor_bonus: float = 0.0
    resist_bonus: float = 0.0
    speed_bonus: int = 0


@dataclass
class Ability:
    id: str
    name: str
    base_damage: float = 20.0
    is_magic: bool = True
    res_pen: float = 0.0
    bonus_prof: float = 1.0
    heal_amount: float = 0.0


@dataclass
class CharacterProfile:
    id: str
    name: str
    max_hp: float
    damage: float
    armor: float
    resist: float
    speed: int = 100
    items: List[Item] = field(default_factory=list)
    abilities: List[Ability] = field(default_factory=list)

    def add_item(self, item: Item) -> None:
        self.items.append(item)

    def add_ability(self, ability: Ability) -> None:
        self.abilities.append(ability)


@dataclass
class Character:
    profile: CharacterProfile
    hp: float
    buffs: List[float] = field(default_factory=list)
    debuffs: List[float] = field(default_factory=list)

    @classmethod
    def from_profile(cls, profile: CharacterProfile) -> "Character":
        return cls(profile=profile, hp=profile.max_hp)

    @property
    def is_alive(self) -> bool:
        return self.hp > 0

    def total_speed(self) -> int:
        return self.profile.speed + sum(i.speed_bonus for i in self.profile.items)

    def total_armor(self) -> float:
        return self.profile.armor + sum(i.armor_bonus for i in self.profile.items)

    def total_resist(self) -> float:
        val = self.profile.resist + sum(i.resist_bonus for i in self.profile.items)
        return max(0.0, min(0.95, val))

    def calc_physical_damage(self, target: "Character", raw_damage: Optional[float] = None) -> float:
        base = raw_damage if raw_damage is not None else self.profile.damage
        after_armor = base - target.total_armor()
        if after_armor <= 0:
            return 0.0
        return round(after_armor * max(0.0, 1.0 - target.total_resist()), 2)

    def calc_magic_damage(self, target: "Character", ability: Ability) -> float:
        flat_bonus = sum(i.flat_damage for i in self.profile.items) + sum(self.buffs)
        prof_bonus = ability.bonus_prof + sum(i.bonus_prof for i in self.profile.items)
        debuff_sum = sum(self.debuffs)

        res_mult = max(0.0, 1.0 - target.total_resist() + ability.res_pen)
        prof_mult = max(0.0, prof_bonus - debuff_sum)
        dmg = (ability.base_damage * res_mult + flat_bonus) * prof_mult
        return round(max(0.0, dmg), 2)

    def attack(self, target: "Character") -> str:
        dmg = self.calc_physical_damage(target)
        target.hp = max(0.0, target.hp - dmg)
        return f"{self.profile.name} атакує {target.profile.name} -> фіз. шкода: {dmg}, HP цілі: {target.hp}"

    def heal(self, target: "Character", amount: float = 15.0) -> str:
        prev = target.hp
        target.hp = min(target.profile.max_hp, target.hp + amount)
        diff = round(target.hp - prev, 2)
        return f"{self.profile.name} лікує {target.profile.name} на +{diff} HP (HP: {target.hp})"

    def action(self, action_type: str, target: "Character", ability_id: Optional[str] = None) -> str:
        if not self.is_alive:
            return f"{self.profile.name} не може виконати дію (HP = 0)"
        if action_type == "attack":
            return self.attack(target)
        if action_type == "heal":
            return self.heal(target)
        if action_type == "ability" and ability_id:
            ability = next((a for a in self.profile.abilities if a.id == ability_id), None)
            if not ability:
                return f"Навичку '{ability_id}' не знайдено у {self.profile.name}"
            if ability.heal_amount > 0:
                return self.heal(target, ability.heal_amount)
            dmg = (
                self.calc_magic_damage(target, ability)
                if ability.is_magic
                else self.calc_physical_damage(target, ability.base_damage)
            )
            target.hp = max(0.0, target.hp - dmg)
            return f"{self.profile.name} застосовує '{ability.name}' до {target.profile.name} -> шкода: {dmg}, HP цілі: {target.hp}"
        return f"Невідома дія '{action_type}'"

    def check_status(self) -> str:
        state = "ЖИВИЙ" if self.is_alive else "ПЕРЕМОЖЕНИЙ"
        return f"{self.profile.name}: {self.hp}/{self.profile.max_hp} HP (SPD {self.total_speed()}) [{state}]"


@dataclass
class TurnRecord:
    turn_number: int
    actor_id: str
    target_id: str
    action_type: str
    message: str


class Turn:
    def __init__(self, turn_number: int, characters: List[Character]):
        self.turn_number = turn_number
        self.characters = characters
        self.records: List[TurnRecord] = []

    def get_turn_order(self) -> List[Character]:
        alive = [c for c in self.characters if c.is_alive]
        ordered = sorted(alive, key=lambda c: c.total_speed(), reverse=True)
        queue = list(ordered)
        for c in ordered:
            extra = max(0, (c.total_speed() - 100) // 100)
            queue.extend([c] * extra)
        return queue

    def act(self, action_id: str, actor: Character, target: Character, ability_id: Optional[str] = None) -> TurnRecord:
        msg = actor.action(action_id, target, ability_id)
        record = TurnRecord(
            turn_number=self.turn_number,
            actor_id=actor.profile.id,
            target_id=target.profile.id,
            action_type=action_id,
            message=msg,
        )
        self.records.append(record)
        return record


class StoragePort(Protocol):
    def save_state(self, raw_json: str) -> None: ...
    def load_state(self) -> Optional[str]: ...


@dataclass
class GameConfig:
    turn_number: int = 1
    characters: List[Character] = field(default_factory=list)
    history: List[TurnRecord] = field(default_factory=list)


class Game:
    def __init__(self, storage: StoragePort):
        self.storage = storage
        self.config: Optional[GameConfig] = None
        self.current_turn: Optional[Turn] = None

    def setup_game(self, profiles: List[CharacterProfile]) -> GameConfig:
        chars = [Character.from_profile(p) for p in profiles]
        self.config = GameConfig(turn_number=1, characters=chars, history=[])
        return self.config

    def start_game(self, config: GameConfig) -> Turn:
        self.config = config
        self.current_turn = Turn(config.turn_number, config.characters)
        return self.current_turn

    def next_turn(self) -> Turn:
        if not self.config:
            raise RuntimeError("Гру не ініціалізовано")
        if self.current_turn:
            self.config.history.extend(self.current_turn.records)
        self.config.turn_number += 1
        self.current_turn = Turn(self.config.turn_number, self.config.characters)
        return self.current_turn

    def add_character_profile(self, profile: CharacterProfile) -> Character:
        char = Character.from_profile(profile)
        if self.config:
            self.config.characters.append(char)
        return char

    def save_game(self) -> None:
        if not self.config:
            return
        full_history = list(self.config.history)
        if self.current_turn:
            full_history.extend(self.current_turn.records)

        payload = {
            "turn_number": self.config.turn_number,
            "history": [asdict(r) for r in full_history],
            "characters": [
                {
                    "hp": c.hp,
                    "buffs": c.buffs,
                    "debuffs": c.debuffs,
                    "profile": asdict(c.profile),
                }
                for c in self.config.characters
            ],
        }
        self.storage.save_state(json.dumps(payload, ensure_ascii=False, indent=2))

    def load_game(self) -> Optional[GameConfig]:
        raw = self.storage.load_state()
        if not raw:
            return None
        data = json.loads(raw)
        chars: List[Character] = []
        for item in data["characters"]:
            p = item["profile"]
            profile = CharacterProfile(
                id=p["id"],
                name=p["name"],
                max_hp=p["max_hp"],
                damage=p["damage"],
                armor=p["armor"],
                resist=p["resist"],
                speed=p.get("speed", 100),
                items=[Item(**i) for i in p.get("items", [])],
                abilities=[Ability(**a) for a in p.get("abilities", [])],
            )
            chars.append(
                Character(
                    profile=profile,
                    hp=item["hp"],
                    buffs=item.get("buffs", []),
                    debuffs=item.get("debuffs", []),
                )
            )
        history = [TurnRecord(**r) for r in data.get("history", [])]
        cfg = GameConfig(turn_number=data["turn_number"], characters=chars, history=history)
        self.config = cfg
        self.current_turn = Turn(cfg.turn_number, cfg.characters)
        return cfg

    def get_history_lines(self) -> List[str]:
        lines = [r.message for r in (self.config.history if self.config else [])]
        if self.current_turn:
            lines.extend(r.message for r in self.current_turn.records)
        return lines