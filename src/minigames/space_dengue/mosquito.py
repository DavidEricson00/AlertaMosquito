"""Mosquito enemy entities for Space Dengue minigame."""

import pygame
import random
from src.core.paths import get_asset_path

MOSQUITO_SPEED = 96
cache = {}

class Mosquito(pygame.sprite.Sprite):
    """Alien mosquito that moves laterally, animates wings, and drops down on boundary contact."""
    def __init__(self, color, x, y):
        super().__init__()
        if color not in cache:
            cache[color] = (
                pygame.image.load(get_asset_path("minigames", "space_dengue", f"mosquito_{color}.png")).convert_alpha(),
                pygame.image.load(get_asset_path("minigames", "space_dengue", f"mosquito_{color}_down.png")).convert_alpha(),
            )
        (self.image1, self.image2) = cache[color]
        self.image = self.image1
        self.rect = self.image.get_rect(topleft=(x, y))
        self.x = x
        self.tempo = random.random()

    def update(self, direction, delta):
        self.x += direction * MOSQUITO_SPEED * delta
        self.rect.x = self.x
        self.tempo += delta
        if self.tempo % 1.0 < 0.5:
            self.image = self.image1
        else:
            self.image = self.image2

class Extra(pygame.sprite.Sprite):
    """Bonus mosquito flying horizontally across top of the screen."""
    def __init__(self, side, screen_width):
        super().__init__()
        self.image = pygame.image.load(get_asset_path("minigames", "space_dengue", "mosquito_yellow.png")).convert_alpha()

        if side == "right":
            x = screen_width + 50
            self.speed = -4
        else:
            x = -50
            self.speed = 4

        self.rect = self.image.get_rect(topleft=(x, 80))

    def update(self):
        self.rect.x += self.speed
