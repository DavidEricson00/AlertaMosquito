from pathlib import Path

# Base directories
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
ASSETS_DIR = PROJECT_ROOT / "assets"
SRC_DIR = PROJECT_ROOT / "src"

def get_asset_path(*subpaths: str) -> str:
    """Return the absolute path string for an asset, ensuring cross-platform compatibility."""
    return str(ASSETS_DIR.joinpath(*subpaths))

# Shared Fonts
FONT_PRESS_START = get_asset_path("fonts", "press_start_2p.ttf")
FONT_MILKS = get_asset_path("fonts", "tt_milks.ttf")

# Shared UI Elements
UI_TIMER_MOSQUITO = get_asset_path("ui", "hud", "timer_mosquito.png")
UI_TIMER_BAR = get_asset_path("ui", "hud", "timer_bar.png")
UI_COIN = get_asset_path("ui", "hud", "coin.png")
UI_MEDAL = get_asset_path("ui", "hud", "medal.png")

UI_DICE = [
    get_asset_path("ui", "dice", "dice_red.png"),
    get_asset_path("ui", "dice", "dice_blue.png"),
    get_asset_path("ui", "dice", "dice_green.png"),
    get_asset_path("ui", "dice", "dice_yellow.png"),
]

UI_NUMBERS = [
    get_asset_path("ui", "numbers", "number_1.png"),
    get_asset_path("ui", "numbers", "number_2.png"),
    get_asset_path("ui", "numbers", "number_3.png"),
    get_asset_path("ui", "numbers", "number_4.png"),
]

# Character Assets
CHARACTER_WALK_SPRITES = [
    get_asset_path("characters", "walk", f"walk_{i}.png") for i in range(1, 5)
]

# Note: Character order in original game is 2, 4, 1, 3
CHARACTER_ICONS = [
    get_asset_path("characters", "icons", "icon_2.png"),
    get_asset_path("characters", "icons", "icon_4.png"),
    get_asset_path("characters", "icons", "icon_1.png"),
    get_asset_path("characters", "icons", "icon_3.png"),
]

CHARACTER_PORTRAITS = [
    get_asset_path("characters", "portraits", "portrait_2.png"),
    get_asset_path("characters", "portraits", "portrait_4.png"),
    get_asset_path("characters", "portraits", "portrait_1.png"),
    get_asset_path("characters", "portraits", "portrait_3.png"),
]
