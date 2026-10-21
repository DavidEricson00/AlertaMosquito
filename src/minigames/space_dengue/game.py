"""Space Dengue minigame: Space Invaders inspired shooter defending against mosquito swarms."""

import pygame
from random import choice, randint
from src.core.paths import get_asset_path
from src.minigames.space_dengue.player import Player
import src.minigames.space_dengue.obstacle as obstacle
from src.minigames.space_dengue.mosquito import Mosquito, Extra, MOSQUITO_SPEED
from src.minigames.space_dengue.laser import Laser

screen_width = 1066
screen_height = 600

class SpaceMinigame:
    """Minigame where the player defends against rows of alien mosquitoes inspired by Space Invaders."""
    tamanho = (screen_width, screen_height)

    def __init__(self):
        self.bg = pygame.image.load(get_asset_path("minigames", "space_dengue", "background.png")).convert_alpha()

        # Player Setup
        player_sprite = Player((screen_width / 2, screen_height), screen_width, 5)
        self.player = pygame.sprite.GroupSingle(player_sprite)

        # Obstacle Setup
        self.blocks = pygame.sprite.Group()
        self.obstacle_amount = 4
        self.obstacle_x_positions = [num * (screen_width / self.obstacle_amount) for num in range(self.obstacle_amount)]
        self.create_multiple_obstacles(screen_width / 15, 320, *self.obstacle_x_positions)

        # Mosquito setup
        self.mosquitos = pygame.sprite.Group()
        self.mosquito_lasers = pygame.sprite.Group()
        self.mosquito_setup(rows=4, cols=6, x_distance=96, y_distance=72, y_offset=0)
        self.mosquito_direction = 1
        self.mosquito_downs = 0

        # Extra Setup
        self.extra = pygame.sprite.GroupSingle()
        self.extra_spawn_time = randint(400, 800)

    def get_tempo_da_perdicao(self, tempo_inicio):
        segundos_restantes = 0
        mosquito_mais_esquerdo = screen_width
        for m in self.mosquitos:
            mosquito_mais_esquerdo = min(mosquito_mais_esquerdo, m.rect.left)
        if self.mosquito_direction == 1:
            mosquito_mais_direito = 0
            for m in self.mosquitos:
                mosquito_mais_direito = max(mosquito_mais_direito, m.rect.right)
            distancia_ate_direita = screen_width - mosquito_mais_direito
            segundos_restantes = distancia_ate_direita / MOSQUITO_SPEED
            mosquito_mais_esquerdo += distancia_ate_direita
        segundos_restantes += mosquito_mais_esquerdo / MOSQUITO_SPEED
        return pygame.time.get_ticks() + segundos_restantes * 1000

    def create_obstacle(self, x_start, y_start, offset_x):
        self.blocks.add(obstacle.Obstacle((x_start + offset_x, y_start)))

    def create_multiple_obstacles(self, x_start, y_start, *offset):
        for offset_x in offset:
            self.create_obstacle(x_start, y_start, offset_x)

    def mosquito_setup(self, rows, cols, x_distance=60, y_distance=48, x_offset=70, y_offset=100):
        for row_index in range(rows):
            for col_index in range(cols):
                x = col_index * x_distance + x_offset
                y = row_index * y_distance + y_offset

                if row_index == 0:
                    mosquito_sprite = Mosquito("yellow", x, y)
                elif 1 <= row_index <= 2:
                    mosquito_sprite = Mosquito("green", x, y)
                else:
                    mosquito_sprite = Mosquito("red", x, y)
                self.mosquitos.add(mosquito_sprite)

    def mosquito_position_checker(self):
        all_mosquitos = self.mosquitos.sprites()
        for m in all_mosquitos:
            if m.rect.right >= screen_width:
                self.mosquito_direction = -1
                self.mosquito_move_down(8)
                break
            elif m.rect.left <= 0:
                self.mosquito_direction = 1
                self.mosquito_move_down(8)
                break

    def mosquito_move_down(self, distance):
        if self.mosquitos:
            for m in self.mosquitos.sprites():
                m.rect.y += distance
        self.mosquito_downs += 1

    def mosquito_shoot(self):
        if self.mosquitos.sprites():
            random_mosquito = choice(self.mosquitos.sprites())
            laser_sprite = Laser(random_mosquito.rect.center, 6, screen_height)
            self.mosquito_lasers.add(laser_sprite)

    def extra_mosquito_timer(self, delta):
        self.extra_spawn_time -= delta * 60
        if self.extra_spawn_time <= 0:
            self.extra.add(Extra(choice(['right', 'left']), screen_width))

    def frame(self, screen, delta, jogo):
        self.player.update(delta)
        self.mosquitos.update(self.mosquito_direction, delta)
        self.mosquito_position_checker()
        self.mosquito_lasers.update(delta)
        self.extra.update()

        if self.mosquito_downs >= 2:
            return "perdeu"

        for laser in self.player.sprite.lasers.sprites():
            for block in self.blocks.sprites():
                if block.rect.colliderect(laser.rect):
                    block.kill()
                    laser.kill()
                    break
            else:
                for m in self.mosquitos.sprites():
                    if m.rect.colliderect(laser.rect):
                        m.kill()
                        laser.kill()
                        break

        for m in self.mosquitos.sprites():
            if m.rect.midbottom[1] >= screen_height * 3 / 4:
                return "perdeu"

        if len(self.mosquitos.sprites()) == 0:
            return "ganhou"

        screen.blit(pygame.transform.scale(self.bg, screen.get_size()), (0, 0))
        self.player.sprite.lasers.draw(screen)
        self.player.draw(screen)
        self.blocks.draw(screen)
        self.mosquitos.draw(screen)
        self.mosquito_lasers.draw(screen)
        self.extra.draw(screen)
