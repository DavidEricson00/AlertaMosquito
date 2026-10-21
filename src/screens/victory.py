"""Victory screen displayed when a player wins the game, featuring animated confetti and character walk."""

import pygame
import random
from src.core.paths import FONT_MILKS, CHARACTER_WALK_SPRITES

font48 = pygame.font.Font(FONT_MILKS, 48)
font64 = pygame.font.Font(FONT_MILKS, 64)

QUANTIDADE_CONFETES = 250


class Confete:
    """Individual animated confetti particle falling down the screen."""
    def __init__(self, largura, altura):
        self.largura = largura
        self.altura = altura
        self.size = random.randint(5, 10)
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.surface = pygame.Surface((self.size, self.size))
        self.surface.fill(self.color)
        self.reset(inicial=True)

    def reset(self, inicial=False):
        self.x = random.uniform(0, self.largura)
        self.y = random.uniform(-self.altura, self.altura) if inicial else random.uniform(-50, -10)
        self.speed_y = random.uniform(60, 180)
        self.sway = random.uniform(-40, 40)

    def update(self, delta):
        self.y += self.speed_y * delta
        self.x += self.sway * delta
        if self.y > self.altura or self.x < -20 or self.x > self.largura + 20:
            self.reset()

    def draw(self, tela):
        tela.blit(self.surface, (self.x, self.y))


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

        tela.fill(self.color)

        self.desenha_texto(tela, self.mensagem, font64, 150)
        self.desenha_texto(tela, self.mensagem1, font48, 220)

        tempo_atual = pygame.time.get_ticks()
        if tempo_atual - self.ultimo_tempo > self.tempo_frame:
            self.frame_atual = (self.frame_atual + 1) % len(self.personagens)
            self.ultimo_tempo = tempo_atual

        scaled_sprite = pygame.transform.scale(
            self.personagens[self.frame_atual].subsurface((self.personagem * 24, 0 * 26, 24, 26)),
            (150, 150)
        )
        sprite_rect = scaled_sprite.get_rect(center=(largura // 2, 350))
        tela.blit(scaled_sprite, sprite_rect.topleft)

        for confete in self.confetes:
            confete.update(delta)
            confete.draw(tela)

        self.tempo += delta
        if self.tempo >= 5:
            return "titulo"


VictoryScreen = FinalTela