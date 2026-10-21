"""Obstacle barriers for Space Dengue minigame."""

import pygame
from src.core.paths import get_asset_path

wall = pygame.image.load(get_asset_path("minigames", "space_dengue", "wall.png")).convert_alpha()

class Obstacle(pygame.sprite.Sprite):
    """Shelter barrier protecting the player from mosquito attacks."""
    def __init__(self, pos):
        super().__init__()
        self.image = wall
        self.rect = self.image.get_rect(topleft=pos)
