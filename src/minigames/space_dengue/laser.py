"""Laser projectile for Space Dengue minigame."""

import pygame
from src.core.paths import get_asset_path

class Laser(pygame.sprite.Sprite):
    """Laser projectile fired upward by player or downward by alien mosquitoes."""
    def __init__(self, pos, speed, screen_height):
        super().__init__()
        self.image = pygame.image.load(get_asset_path("minigames", "space_dengue", "laser.png")).convert_alpha()
        self.rect = self.image.get_rect(bottomright=pos)
        self.speed = speed
        self.height_y_constraint = screen_height

    def destroy(self):
        if self.rect.y <= -50 or self.rect.y >= self.height_y_constraint + 50:
            self.kill()

    def update(self, delta):
        self.rect.y += self.speed * delta * 60
        self.destroy
