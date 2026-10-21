"""Minigames package exporting all four dengue battle minigames."""

from src.minigames.pistol_mosquito import PistolMosquito
from src.minigames.water_drop import PingoMinigame, WaterDropMinigame
from src.minigames.space_dengue import SpaceMinigame
from src.minigames.runner import WalkMinigame, RunnerMinigame

ALL_MINIGAMES = [
    PingoMinigame,
    WalkMinigame,
    SpaceMinigame,
    PistolMosquito,
]
