"""Runner minigame: run and jump or duck over trash, bucket and tire breeding grounds in rhythm."""

import pygame
import math
from random import choice, randint
from src.core.paths import get_asset_path

ANIMATION_SPEED = 0.05

class Player(pygame.sprite.Sprite):
    """Running character with animated run frames."""
    def __init__(self):
        super().__init__()
        self.images = [
            pygame.image.load(get_asset_path("minigames", "runner", f"runboy_{i}.png")).convert_alpha()
            for i in range(1, 5)
        ]
        self.speed = 1.0
        self.image_index = 0
        self.image = self.images[self.image_index]
        self.rect = self.image.get_rect(midbottom=(120, 474))

    def update(self):
        self.image_index += self.speed * ANIMATION_SPEED
        if self.image_index >= len(self.images):
            self.image_index = 0
        self.image = self.images[int(self.image_index)]

object_images = {
    'down': pygame.image.load(get_asset_path("minigames", "runner", "obstacle_bucket_down.png")).convert_alpha(),
    'up': pygame.image.load(get_asset_path("minigames", "runner", "obstacle_trash_up.png")).convert_alpha(),
    'right': pygame.image.load(get_asset_path("minigames", "runner", "obstacle_tire_right.png")).convert_alpha()
}

class Obstacle(pygame.sprite.Sprite):
    """Breeding ground obstacle requiring a specific directional key press to clear."""
    directions = {
        'down': [pygame.K_DOWN, pygame.K_s],
        'up': [pygame.K_UP, pygame.K_w],
        'right': [pygame.K_RIGHT, pygame.K_d]
    }

    def __init__(self, obj_type, minigame, index, posicao_anterior):
        super().__init__()
        self.minigame = minigame
        self.object = obj_type
        self.index = index
        self.image = object_images[obj_type]
        self.posicao_base = posicao_anterior + randint(200, 400) + index * 8
        self.rect = self.image.get_rect(midbottom=(self.posicao_base, 474))

    def update(self):
        if not self.minigame.trigger:
            return
        keys = pygame.key.get_pressed()

        if self.index == self.minigame.kills and self.rect.x <= 720 and self.minigame.stun_timer == 0.0:
            direction_pressed = "none"
            if keys[self.directions["up"][0]] or keys[self.directions["up"][1]]:
                direction_pressed = "up"
            elif keys[self.directions["right"][0]] or keys[self.directions["right"][1]]:
                direction_pressed = "right"
            elif keys[self.directions["down"][0]] or keys[self.directions["down"][1]]:
                direction_pressed = "down"

            if direction_pressed == self.object:
                self.kill()
                self.minigame.kills += 1
                self.minigame.trigger = False
            elif direction_pressed != "none":
                self.minigame.stun_timer = 1.0

def parallax_blit(screen, obj, camera, factor, width):
    """Blit two repeating copies of a background layer for parallax scrolling."""
    screen.blit(obj, (-camera * factor % width, 0))
    screen.blit(obj, (-camera * factor % width - width, 0))

class WalkMinigame:
    """Endless runner rhythm minigame where player runs through city clearing standing water hazards."""
    tamanho = (1280, 720)

    def __init__(self):
        self.fonte = pygame.font.Font(None, 64)
        self.spawn = True
        self.trigger = False
        self.posicao = 0.0
        self.velocidade = 320
        self.stun_timer = 0.0
        self.kills = 0

        self.player = Player()
        self.obstacles = pygame.sprite.Group()

        # Scenery parallax layers
        self.clouds = pygame.image.load(get_asset_path("minigames", "runner", "clouds.png")).convert_alpha()
        self.clouds_rect = self.clouds.get_rect(topleft=(0, 0))

        self.background = pygame.image.load(get_asset_path("minigames", "runner", "background.png")).convert_alpha()
        self.background_rect = self.background.get_rect(topleft=(0, 0))

        self.ground = pygame.image.load(get_asset_path("minigames", "runner", "ground.png")).convert_alpha()
        self.ground_rect = self.ground.get_rect(bottomleft=(0, 720))

        # Directional key hint sprites
        self.upkey = pygame.image.load(get_asset_path("minigames", "runner", "key_up.png")).convert_alpha()
        self.downkey = pygame.image.load(get_asset_path("minigames", "runner", "key_down.png")).convert_alpha()
        self.rightkey = pygame.image.load(get_asset_path("minigames", "runner", "key_right.png")).convert_alpha()

    def get_tempo_da_perdicao(self, tempo_inicio):
        if len(self.obstacles) == 0:
            return 0
        distancia = self.obstacles.sprites()[-1].rect.x - 160
        velocidade_final = math.sqrt(self.velocidade * self.velocidade + 2 * 42 * distancia)
        return pygame.time.get_ticks() + distancia / ((velocidade_final + self.velocidade) / 2) * 1000

    def event(self, event):
        if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
            self.trigger = True

    def frame(self, screen, delta, jogo):
        self.player.update()

        if self.stun_timer > 0.0:
            self.stun_timer -= delta * 4
            if self.stun_timer < 0.0:
                self.stun_timer = 0.0

        if self.spawn:
            posicao_anterior = 600
            for i in range(20):
                obs = Obstacle(choice(['up', 'down', 'right']), self, i, posicao_anterior)
                self.obstacles.add(obs)
                posicao_anterior = obs.posicao_base
            self.spawn = False

        self.velocidade += 42 * delta
        self.posicao += self.velocidade * delta
        self.player.speed = self.velocidade / 500.0

        screen.fill('#87CEEB')
        width = screen.get_width()

        parallax_blit(screen, self.clouds, self.posicao, 0.5, width)
        parallax_blit(screen, self.background, self.posicao, 0.75, width)
        parallax_blit(screen, self.ground, self.posicao, 1.0, width)

        screen.blit(self.player.image, self.player.rect)

        self.obstacles.update()
        self.obstacles.draw(screen)
        active_obj = "none"

        for sprite in self.obstacles.sprites():
            sprite.rect = sprite.image.get_rect(midbottom=(sprite.posicao_base - self.posicao, 474))
            if active_obj == "none":
                if sprite.rect.x <= 160:
                    return "perdeu"
                elif sprite.rect.x <= 720:
                    active_obj = sprite.object

        match active_obj:
            case "up":
                screen.blit(self.upkey, self.upkey.get_rect(midbottom=self.obstacles.sprites()[0].rect.midtop))
            case "down":
                screen.blit(self.downkey, self.downkey.get_rect(midbottom=self.obstacles.sprites()[0].rect.midtop))
            case "right":
                screen.blit(self.rightkey, self.rightkey.get_rect(midbottom=self.obstacles.sprites()[0].rect.midtop))

        if self.kills >= 20:
            return "ganhou"

RunnerMinigame = WalkMinigame
