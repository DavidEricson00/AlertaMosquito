"""Pistol Mosquito minigame: click flying mosquitoes before the timer runs out to protect the vein."""

import pygame
import random
import time
from src.core.paths import get_asset_path

# Load assets
mosquito_image = pygame.image.load(get_asset_path("minigames", "pistol_mosquito", "mosquito_flying.png")).convert_alpha()
bg = pygame.image.load(get_asset_path("minigames", "pistol_mosquito", "background.png")).convert_alpha()
vea = pygame.image.load(get_asset_path("minigames", "pistol_mosquito", "vein.png")).convert_alpha()

screen_width = 1066
screen_height = 600
font = pygame.font.Font(None, 74)

def mouse_logico(pos):
    janela = pygame.display.get_surface()
    largura, altura = janela.get_size()
    return (pos[0] * screen_width / largura, pos[1] * screen_height / altura)

class Mosquito:
    """Individual flying mosquito entity that falls and inverts when shot."""
    def __init__(self):
        self.active = True
        self.atirou = None
        self.fire_duration = 0.2
        self.size = int(mosquito_image.get_width() * 1.5)
        self.x = random.randint(0, screen_width - self.size)
        self.y = random.randint(0, screen_height - self.size)
        self.mosquito_rect = pygame.Rect(self.x, self.y, self.size, self.size)
        self.speed_x = random.choice([2, 2])
        self.speed_y = random.choice([2, 2])
        self.falling = False
        self.inverted = False
        self.gravity = 0.1
        self.velocity_y = 0

    def move(self):
        if not self.active and self.falling:
            self.velocity_y += self.gravity
            self.y += self.velocity_y
            if self.y >= screen_height - mosquito_image.get_height():
                self.y = screen_height - mosquito_image.get_height()
                self.falling = False

        if self.active:
            self.x += self.speed_x
            self.y += self.speed_y
            self.mosquito_rect.topleft = (self.x, self.y)

            if self.x <= 0 or self.x >= screen_width - mosquito_image.get_width():
                self.speed_x = -self.speed_x

            if self.y <= 0 or self.y >= screen_height - mosquito_image.get_height():
                self.speed_y = -self.speed_y

    def draw(self, screen):
        if self.active:
            screen.blit(mosquito_image, (self.x, self.y))

        if self.atirou and (time.time() - self.atirou < self.fire_duration):
            mosquito_invertido = pygame.transform.flip(mosquito_image, True, True)
            screen.blit(mosquito_invertido, (self.x, self.y))
            self.inverted = True
            self.falling = True
        elif not self.active and self.inverted:
            mosquito_invertido = pygame.transform.flip(mosquito_image, True, True)
            screen.blit(mosquito_invertido, (self.x, self.y))

    def deactivate(self):
        self.active = False
        self.atirou = time.time()
        self.falling = True

class Veia:
    """Player-controlled vein tracking mouse horizontal position at the bottom of the screen."""
    def __init__(self, scale_factor=3):
        tamanho = (int(vea.get_width() * scale_factor), int(vea.get_height() * scale_factor))
        self.image = pygame.transform.scale(vea, tamanho)
        self.rect = self.image.get_rect()
        self.rect.centery = screen_height * 0.85

    def update(self):
        mouse_x, _ = mouse_logico(pygame.mouse.get_pos())
        self.rect.centerx = int(mouse_x)

    def draw(self, screen):
        screen.blit(self.image, self.rect)

Vein = Veia

class PistolMosquito:
    """Minigame where the player clicks mosquitoes to swat them within the time limit."""
    tamanho = (screen_width, screen_height)

    def __init__(self):
        self.mosquitos = [Mosquito() for _ in range(10)]
        self.start_time = time.time()
        self.timer_duration = 8
        self.veia = Veia()
        self.pontos = 0

    def event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.atirar(event.pos)

    def atirar(self, posicao_click):
        for mosquito in self.mosquitos:
            if mosquito.active and mosquito.mosquito_rect.collidepoint(posicao_click):
                mosquito.deactivate()
                self.pontos += 1

    def get_tempo_da_perdicao(self, tempo_inicio):
        return tempo_inicio + self.timer_duration * 1000

    def frame(self, screen, delta, jogo):
        elapsed_time = time.time() - self.start_time
        screen.blit(pygame.transform.scale(bg, (screen_width, screen_height)), (0, 0))

        self.veia.update()

        # Polished score badge
        score_str = f"Pontos: {self.pontos}"
        st_s = font.render(score_str, True, (255, 255, 255))
        st_sh = font.render(score_str, True, (0, 0, 0))
        badge_w = st_s.get_width() + 24
        badge_h = st_s.get_height() + 8
        pygame.draw.rect(screen, (0, 0, 0, 120), (10, 10, badge_w, badge_h), border_radius=12)
        pygame.draw.rect(screen, (230, 45, 45), (10, 10, badge_w, badge_h), width=3, border_radius=12)
        screen.blit(st_sh, (26 + 2, 18 + 2))
        screen.blit(st_s, (26, 18))

        if elapsed_time < self.timer_duration:
            for mosquito in self.mosquitos:
                mosquito.move()
                mosquito.draw(screen)

            for mosquito in self.mosquitos:
                if mosquito.active:
                    break
            else:
                return "ganhou"
        else:
            for mosquito in self.mosquitos:
                mosquito.deactivate()
            text = font.render("Você perdeu", True, (255, 0, 0))
            screen.blit(text, (screen_width // 2 - text.get_width() // 2, screen_height // 2 - text.get_height() // 1))
            if elapsed_time >= self.timer_duration + 2:
                return "perdeu"

        self.veia.draw(screen)