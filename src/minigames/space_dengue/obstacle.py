"""Obstacle barriers for Space Dengue minigame."""

import pygame
from src.core.paths import get_asset_path

wall = pygame.image.load(get_asset_path("minigames", "space_dengue", "wall.png")).convert_alpha()

shape = [
    '  xxxxxxx  ',
    ' xxxxxxxxx ',
    'xxxxxxxxxxx',
    'xxxxxxxxxxx',
    'xxxxxxxxxxx',
    'xxx     xxx',
    'xx       xx'
]

class Block(pygame.sprite.Sprite):
    """Subsurface block component of a destructible shelter."""
    def __init__(self, size, color, x, y, row, col):
        super().__init__()
        self.image = pygame.transform.scale(
            wall, (size * len(shape[0]), size * len(shape))
        ).subsurface(pygame.Rect(col * size, row * size, size, size))
        self.rect = self.image.get_rect(topleft=(x, y))

class Obstacle(pygame.sprite.Sprite):
    """Shelter barrier protecting the player from mosquito attacks."""
    def __init__(self, pos):
        super().__init__()
        self.image = wall
        self.rect = self.image.get_rect(topleft=pos)
