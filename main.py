"""Alerta Mosquito - Main Game Entry Point.

Educational board game with action minigames to teach dengue prevention.
"""

import sys
import random
import pygame

# Initialize Pygame and main window
pygame.init()
from src.core.config import WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_CAPTION
from src.core.paths import get_asset_path, UI_TIMER_MOSQUITO, UI_TIMER_BAR

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.RESIZABLE, 0, 0, 1)
screen.set_alpha(None)
pygame.display.set_caption(WINDOW_CAPTION)
clock = pygame.time.Clock()

# Render loading splash
loading = pygame.image.load(get_asset_path("screens", "title", "loading.jpg"))
screen.blit(pygame.transform.scale(loading, screen.get_size()), (0, 0))
pygame.display.update()

# Import game systems
import src.core.utils as util
from src.core.player import Jogo
from src.screens.title import Titulo
from src.screens.character_select import Selecion
from src.screens.board import Tabuleiro
from src.screens.victory import FinalTela
from src.minigames import ALL_MINIGAMES

minigames = ALL_MINIGAMES

modo = Titulo()
tela_minigame = None
tempo_inicio_minigame = 0
delta = 1 / 60

# Timer UI elements for minigames
mosquiton = pygame.image.load(UI_TIMER_MOSQUITO).convert_alpha()
barra = pygame.image.load(UI_TIMER_BAR).convert_alpha()

jogo = Jogo()
casas = None

pygame.event.clear()

def main():
    global modo, tela_minigame, tempo_inicio_minigame, delta, jogo, casas

    while True:
        # Mouse coordinate scaling
        util.mouse_pos = pygame.mouse.get_pos()
        if tela_minigame is not None:
            util.mouse_pos = (
                util.mouse_pos[0] * modo.tamanho[0] / screen.get_width(),
                util.mouse_pos[1] * modo.tamanho[1] / screen.get_height()
            )

        # Event handling
        for event in pygame.event.get():
            if getattr(modo, "event", None) is not None:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    event.pos = util.mouse_pos
                if modo.event(event):
                    continue
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()

        # Keyboard state update
        pressionado_novo = pygame.key.get_pressed()
        util.pressionado_agora = []
        for i in range(len(pressionado_novo)):
            util.pressionado_agora.append(pressionado_novo[i] and not util.pressionado[i])
        util.pressionado = pressionado_novo

        # Frame processing
        util.clear_cache()
        resultado = modo.frame(tela_minigame or screen, delta, jogo)

        # Minigame scaling and HUD overlay
        if tela_minigame:
            if getattr(modo, "smooth", False):
                screen.blit(pygame.transform.smoothscale(tela_minigame, screen.get_size()), (0, 0))
            else:
                screen.blit(pygame.transform.scale(tela_minigame, screen.get_size()), (0, 0))

            size = 0.2
            height = screen.get_height() * size
            char_size = height

            screen.blit(
                pygame.transform.scale(jogo.jogadores[jogo.jogador_atual].get_icone(), (char_size, char_size)),
                pygame.Rect(screen.get_width() - char_size, screen.get_height() - char_size, char_size, height)
            )

        # Minigame doom timer bar
        if getattr(modo, "get_tempo_da_perdicao", None):
            tempo_da_perdicao = modo.get_tempo_da_perdicao(tempo_inicio_minigame)
            t = min((pygame.time.get_ticks() - tempo_inicio_minigame) / (tempo_da_perdicao - tempo_inicio_minigame), 1)
            if t < 0:
                t = 1

            mosquito_width = height * mosquiton.get_width() / mosquiton.get_height()
            screen.blit(
                pygame.transform.scale(mosquiton, (mosquito_width, height)),
                pygame.Rect(0, screen.get_height() - height, mosquito_width, height)
            )
            barra_width = (screen.get_width() - mosquito_width - char_size) * t
            screen.blit(
                pygame.transform.scale(barra, (barra_width, height)),
                pygame.Rect(mosquito_width, screen.get_height() - height, barra_width, height)
            )

        # Game state machine transitions
        match resultado:
            case "titulo":
                jogo = Jogo()
                modo = Titulo()
                tela_minigame = None
            case "selecion":
                jogo = Jogo()
                jogo.jogador_atual = 0
                modo = Selecion(None, jogo)
                tela_minigame = None
            case "venceu":
                modo = FinalTela(jogo.jogador_atual, jogo.jogadores[jogo.jogador_atual].personagem)
                tela_minigame = None
            case "iniciar jogo":
                modo = Tabuleiro(None, jogo)
                casas = modo.casas
                tela_minigame = None
            case "minigame":
                modo = random.choice(minigames)()
                tela_minigame = pygame.Surface(modo.tamanho)
                tempo_inicio_minigame = pygame.time.get_ticks()
            case "minigame0":
                modo = minigames[0]()
                tela_minigame = pygame.Surface(modo.tamanho)
                tempo_inicio_minigame = pygame.time.get_ticks()
            case "minigame1":
                modo = minigames[1]()
                tela_minigame = pygame.Surface(modo.tamanho)
                tempo_inicio_minigame = pygame.time.get_ticks()
            case "minigame2":
                modo = minigames[2]()
                tela_minigame = pygame.Surface(modo.tamanho)
                tempo_inicio_minigame = pygame.time.get_ticks()
            case "minigame3":
                modo = minigames[3]()
                tela_minigame = pygame.Surface(modo.tamanho)
                tempo_inicio_minigame = pygame.time.get_ticks()
            case "ganhou":
                jogo.receber_moedas(10)
                jogo.passar_vez()
                modo = Tabuleiro(casas, jogo)
                tela_minigame = None
            case "perdeu":
                jogo.passar_vez()
                modo = Tabuleiro(casas, jogo)
                tela_minigame = None

        pygame.display.update()
        delta = clock.tick() / 1000

if __name__ == '__main__':
    main()