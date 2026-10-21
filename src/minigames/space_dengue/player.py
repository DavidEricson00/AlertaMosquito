"""Player cannon entity for Space Dengue minigame."""

import pygame
from src.core.paths import get_asset_path
from src.minigames.space_dengue.laser import Laser

class Player(pygame.sprite.Sprite):
    """Player-controlled sprayer firing upward against approaching mosquitoes."""
    def __init__(self, pos, constraint, speed):
        super().__init__()
        self.atirando = pygame.image.load(get_asset_path("minigames", "space_dengue", "player.png")).convert_alpha()
        self.andando = [
            pygame.image.load(get_asset_path("minigames", "space_dengue", "player_walk_a.png")).convert_alpha(),
            pygame.image.load(get_asset_path("minigames", "space_dengue", "player_walk_b.png")).convert_alpha()
        ]
        self.image = self.atirando
        self.rect = self.image.get_rect(midbottom=pos)
        self.speed = speed
        self.max_x_constraint = constraint
        self.ready = True
        self.laser_time = 0
        self.laser_cooldown = 300
        self.x = self.rect.x
        self.lasers = pygame.sprite.Group()
        self.tempo = 0.0

    def get_input(self, delta):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.x += self.speed * 200 * delta
            self.image = self.andando[int(pygame.time.get_ticks() % 500 / 250)]
        elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.x -= self.speed * 200 * delta
            self.image = self.andando[int(pygame.time.get_ticks() % 500 / 250)]
            self.image = pygame.transform.flip(self.image, True, False)
        self.rect.x = self.x

        if self.ready:
            self.shoot_laser()
            self.ready = False
            self.laser_time = pygame.time.get_ticks()
            self.image = self.atirando

    def recharge(self):
        if not self.ready:
            current_time = pygame.time.get_ticks()
            if current_time - self.laser_time >= self.laser_cooldown:
                self.ready = True

    def constraint(self):
        if self.rect.left <= 0:
            self.rect.left = 0
            self.x = self.rect.x
        elif self.rect.right >= self.max_x_constraint:
            self.rect.right = self.max_x_constraint
            self.x = self.rect.x

    def shoot_laser(self):
        self.lasers.add(Laser(self.rect.center, -20, self.rect.bottom))

    def update(self, delta):
        self.tempo += delta
        self.get_input(delta)
        self.constraint()
        self.recharge()
        self.lasers.update(delta)
