from core.game_engine import Ability, CharacterProfile, Game, Item
from stubs.storage_stub import JsonFileStorageStub
from core.catalog_mapper import CatalogMapper
from stubs.genshin_api_stub import GenshinApiClientOrStub


def run_text_game_demo() -> None:
    storage = JsonFileStorageStub("save_game.json")
    game = Game(storage)

    hero_profile = CharacterProfile(
        id="hero",
        name="Аетер",
        max_hp=120,
        damage=35,
        armor=10,
        resist=0.1,
        speed=200,
        items=[Item(id="sword", name="Клинок вітру", flat_damage=5.0, bonus_prof=0.2)],
        abilities=[Ability(id="spark", name="Іскра", base_damage=25.0, is_magic=True, res_pen=0.1, bonus_prof=1.0)],
    )
    enemy_profile = CharacterProfile(
        id="slime",
        name="Кам'яний вартовий",
        max_hp=150,
        damage=25,
        armor=15,
        resist=0.2,
        speed=100,
    )

    cfg = game.setup_game([hero_profile, enemy_profile])
    turn = game.start_game(cfg)

    hero, enemy = cfg.characters[0], cfg.characters[1]
    print("Черга дій:", [c.profile.name for c in turn.get_turn_order()])

    turn.act("attack", hero, enemy)
    turn.act("ability", hero, enemy, ability_id="spark")
    turn.act("attack", enemy, hero)

    mage_profile = CharacterProfile(id="mage", name="Ліза", max_hp=90, damage=20, armor=5, resist=0.15, speed=150)
    game.add_character_profile(mage_profile)

    game.next_turn()
    game.save_game()

    print("\n--- Історія кроків ---")
    for line in game.get_history_lines():
        print(line)

    restored_game = Game(storage)
    restored_cfg = restored_game.load_game()
    print("\nВідновлений номер кроку:", restored_cfg.turn_number if restored_cfg else None)


def run_catalog_demo() -> None:
    client = GenshinApiClientOrStub(use_live_api=True)
    ids = client.get_character_ids()[:2]
    print("\n--- Каталог персонажів ---")
    for char_id in ids:
        raw = client.get_character_raw(char_id)
        vm_model = CatalogMapper.map_character(raw, fallback_id=char_id)
        print(vm_model)


if __name__ == "__main__":
    run_text_game_demo()
    run_catalog_demo()