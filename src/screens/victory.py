"""Victory screen displayed when a player wins the game, featuring animated confetti and character walk."""

import pygame
import random
import math
from src.core.paths import FONT_MILKS, CHARACTER_WALK_SPRITES

font48 = pygame.font.Font(FONT_MILKS, 48)
font64 = pygame.font.Font(FONT_MILKS, 64)

QUANTIDADE_CONFETES = 250


CONFETTI_COLORS = [
    (255, 215, 0),    # Sunny Gold
    (50, 180, 255),   # Sky Blue
    (255, 95, 130),   # Coral Pink
    (45, 215, 95),    # Emerald Green
    (180, 100, 255),  # Violet
    (255, 145, 30),   # Bright Orange
    (255, 255, 255),  # Crisp White
]

class Confete:
    """Festive animated confetti ribbons and circles drifting down the screen."""
    def __init__(self, largura, altura):
        self.largura = largura
        self.altura = altura
        self.reset(inicial=True)

    def reset(self, inicial=False):
        self.x = random.uniform(0, self.largura)
        self.y = random.uniform(-self.altura, self.altura) if inicial else random.uniform(-50, -10)
        self.speed_y = random.uniform(70, 200)
        self.sway = random.uniform(-50, 50)
        self.sway_phase = random.uniform(0, 6.28)
        self.color = random.choice(CONFETTI_COLORS)
        self.is_circle = random.random() < 0.35
        self.w = random.randint(6, 12)
        self.h = random.randint(4, 9) if not self.is_circle else self.w

    def update(self, delta):
        self.sway_phase += delta * 4
        self.y += self.speed_y * delta
        self.x += (self.sway + 30 * math.sin(self.sway_phase)) * delta
        if self.y > self.altura + 20 or self.x < -30 or self.x > self.largura + 30:
            self.reset()

    def draw(self, tela):
        if self.is_circle:
            pygame.draw.circle(tela, self.color, (int(self.x), int(self.y)), self.w // 2)
        else:
            pygame.draw.rect(tela, self.color, (int(self.x), int(self.y), self.w, self.h), border_radius=2)


class FinalTela:
    """Victory screen controller celebrating the winning player."""
    tamanho = (1066, 600)

    def __init__(self, numero, personagem):
        self.color = (218, 165, 32)
        self.mensagem = "Fim de Jogo"
        self.mensagem1 = f"Parabéns ao Jogador {numero + 1}!"
        self.numero = numero
        self.personagem = personagem

        self.personagens = [
            pygame.image.load(path).convert_alpha() for path in CHARACTER_WALK_SPRITES
        ]

        self.confetes = []
        self.tamanho_confete = None

        self.frame_atual = 0
        self.tempo_frame = 250
        self.ultimo_tempo = pygame.time.get_ticks()
        self.tempo = 0.0

    def desenha_texto(self, tela, texto, fonte, y):
        text_surface = fonte.render(texto, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(tela.get_width() // 2, y))
        tela.blit(text_surface, text_rect.topleft)

    def frame(self, tela, delta, jogo):
        largura, altura = tela.get_size()

        if self.tamanho_confete != (largura, altura):
            self.tamanho_confete = (largura, altura)
            self.confetes = [Confete(largura, altura) for _ in range(QUANTIDADE_CONFETES)]

        # Festive golden sun background
        tela.fill((250, 196, 48))

        # Confetti background layer
        for confete in self.confetes:
            confete.update(delta)
            confete.draw(tela)

        center_x = largura // 2

        # Header card banner
        banner_rect = pygame.Rect(center_x - 380, 32, 760, 136)
        pygame.draw.rect(tela, (25, 35, 60), banner_rect, border_radius=24)
        pygame.draw.rect(tela, (255, 215, 60), banner_rect, width=4, border_radius=24)

        # Title: FIM DE JOGO
        t_s = font64.render("FIM DE JOGO!", True, (255, 220, 60))
        t_sh = font64.render("FIM DE JOGO!", True, (0, 0, 0))
        tela.blit(t_sh, (center_x - t_s.get_width() // 2 + 2, 46 + 2))
        tela.blit(t_s, (center_x - t_s.get_width() // 2, 46))

        # Subtitle: Parabéns ao Jogador X! (correct UTF-8 encoding)
        parabens_txt = f"Parabéns ao Jogador {self.numero + 1}!"
        s_s = font48.render(parabens_txt, True, (255, 255, 255))
        s_sh = font48.render(parabens_txt, True, (0, 0, 0))
        tela.blit(s_sh, (center_x - s_s.get_width() // 2 + 2, 112 + 2))
        tela.blit(s_s, (center_x - s_s.get_width() // 2, 112))

        # Winner Podium
        podium_rect = pygame.Rect(center_x - 130, 420, 260, 90)
        pygame.draw.rect(tela, (215, 145, 20), (center_x - 134, 424, 268, 92), border_radius=18)
        pygame.draw.rect(tela, (255, 225, 80), podium_rect, border_radius=18)
        pygame.draw.rect(tela, (255, 255, 255), (center_x - 120, 428, 240, 10), border_radius=5)

        num1_surf = font64.render("1º", True, (160, 90, 10))
        tela.blit(num1_surf, (center_x - num1_surf.get_width() // 2, 436))

        # Character animation on podium
        tempo_atual = pygame.time.get_ticks()
        if tempo_atual - self.ultimo_tempo > self.tempo_frame:
            self.frame_atual = (self.frame_atual + 1) % len(self.personagens)
            self.ultimo_tempo = tempo_atual

        scaled_sprite = pygame.transform.scale(
            self.personagens[self.frame_atual].subsurface((self.personagem * 24, 0 * 26, 24, 26)),
            (160, 160)
        )
        tela.blit(scaled_sprite, (center_x - 80, 270))

        # Bottom return hint
        hint_s = font48.render("Voltando ao menu principal...", True, (120, 75, 15))
        tela.blit(hint_s, (center_x - hint_s.get_width() // 2, 545))

        self.tempo += delta
        if self.tempo >= 5:
            return "titulo"


VictoryScreen = FinalTela