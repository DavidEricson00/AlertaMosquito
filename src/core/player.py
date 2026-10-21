"""Player and game state models."""

import pygame
import src.core.utils as utils

class Jogador:
    """Represents a player in the board game, their chosen character, position, and inventory."""
    numero = 0
    personagem = None
    moedas = 0
    medalhas = 0
    medalha_y = 50
    casa = (0, 0)
    direcao = (1, 0)

    def get_icone(self):
        """Return the portrait icon for this player's selected character."""
        return utils.icones[self.personagem]

    def get_andamento(self, direcao, parado=False):
        """Return the walking animation surface for this character facing the given direction."""
        out = pygame.Surface((24, 24), pygame.SRCALPHA)
        if not isinstance(direcao, str):
            if direcao[0] < 0:
                direcao = "left"
            elif direcao[0] > 0:
                direcao = "right"
            elif direcao[1] < 0:
                direcao = "up"
            else:
                direcao = "down"

        # Spritesheet slicing for character walk animations
        match direcao:
            case "down":
                frame_idx = 1 if parado else pygame.time.get_ticks() // 150 % 4
                out.blit(utils.andamentos[frame_idx], (0, 0), (self.personagem * 24, 0 * 26, 24, 26))
            case "up":
                frame_idx = 1 if parado else pygame.time.get_ticks() // 150 % 4
                out.blit(utils.andamentos[frame_idx], (0, 0), (self.personagem * 24, 1 * 26, 24, 26))
            case "right":
                frame_idx = 1 if parado else pygame.time.get_ticks() // 150 % 4
                out.blit(utils.andamentos[frame_idx], (0, 0), (self.personagem * 24, 2 * 26, 24, 26))
            case "left":
                frame_idx = 1 if parado else pygame.time.get_ticks() // 150 % 4
                out.blit(utils.andamentos[frame_idx], (0, 0), (self.personagem * 24, 3 * 26, 24, 26))
        return out

class Jogo:
    """Session state for the active match, managing turn rotation, coin balance and player list."""
    jogadores = [Jogador()]
    for i in range(len(jogadores)):
        jogadores[i].numero = i
    jogadores[0].personagem = 0
    jogador_atual = 0

    def __init__(self):
        self.jogador_atual = 0

    def passar_vez(self):
        """Pass turn to the next player."""
        self.jogador_atual += 1
        if self.jogador_atual >= len(self.jogadores):
            self.jogador_atual = 0

    def receber_moedas(self, moedas):
        """Award coins to the current active player."""
        self.jogadores[self.jogador_atual].moedas += moedas

    def perder_moedas(self, moedas):
        """Deduct coins from the current active player, preventing negative balance."""
        self.jogadores[self.jogador_atual].moedas = max(self.jogadores[self.jogador_atual].moedas - moedas, 0)

# English aliases for standard naming convention
Player = Jogador
Game = Jogo
