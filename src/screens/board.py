"""Main game board screen handling map rendering, dice rolling, player movement, trivia cards, and camera."""

import pygame
import random
import math
import src.core.utils as utils
import src.screens.trivia as perguntas
from src.core.config import PLAYER_BORDER_COLORS
from src.core.paths import (
    get_asset_path, FONT_PRESS_START, UI_MEDAL, UI_COIN, UI_DICE
)

# Board tile sizing constants
CASA_SIZE = 80
CASA_STRIDE = CASA_SIZE + 8

# Tile types distribution
TIPOS = [
    "+R$5", "+R$5", "+R$5",
    "-R$2",
    "dado", "dado",
    "carta", "carta", "carta",
    "minigame", "minigame", "minigame",
    "teleporte"
]

MAPA = [
    "                  ",
    "                  ",
    "                  ",
    "                  ",
    "    MXXXX   XXXXM ",
    "    X   X   X   X ",
    "    X   X   X   X ",
    "    X   X   X   X ",
    "    XXXXMXXXMXXXX ",
    "        X   X     ",
    "        X   X     ",
    "        X   X     ",
    "    XXXXMXXXMXXXX ",
    "    X   X   X   X ",
    "    X   X   X   X ",
    "    X   X   X   X ",
    "    MXXXX   XXXXM ",
    "                  "
]

# Load Board Visual Assets
fundo = pygame.image.load(get_asset_path("screens", "board", "map_floor.png")).convert_alpha()
objetos = [
    pygame.image.load(get_asset_path("screens", "board", f"map_objects_{i}.png")).convert_alpha()
    for i in range(5)
]

portal = pygame.transform.smoothscale(pygame.image.load(get_asset_path("screens", "board", "portal.png")).convert_alpha(), (256, 256))
cinero = pygame.transform.smoothscale(pygame.image.load(get_asset_path("screens", "board", "ashtray.png")).convert_alpha(), (256, 256))
lixo = pygame.transform.smoothscale(pygame.image.load(get_asset_path("screens", "board", "trash.png")).convert_alpha(), (256, 256))
dado = pygame.transform.smoothscale(pygame.image.load(get_asset_path("screens", "board", "dice.png")).convert_alpha(), (256, 256))
minigame = pygame.transform.smoothscale(pygame.image.load(get_asset_path("screens", "board", "minigame.png")).convert_alpha(), (256, 256))
medalha = pygame.transform.smoothscale(pygame.image.load(get_asset_path("screens", "board", "medal.png")).convert_alpha(), (256, 256))
medalhas = pygame.transform.smoothscale(pygame.image.load(UI_MEDAL).convert_alpha(), (160, 160))
carta = pygame.transform.smoothscale(pygame.image.load(get_asset_path("screens", "board", "card.png")).convert_alpha(), (256, 256))
cartabg = pygame.image.load(get_asset_path("screens", "board", "card_bg.png")).convert_alpha()
interrogacao = pygame.transform.smoothscale(pygame.image.load(get_asset_path("screens", "board", "question_mark.webp")).convert_alpha(), (160, 160))
seta = pygame.image.load(get_asset_path("screens", "board", "arrow.png")).convert_alpha()
moedinha = pygame.transform.smoothscale_by(pygame.image.load(UI_COIN).convert_alpha(), 0.1)
moedinha_black = utils.tint_mult(moedinha, "black")

fonte = pygame.font.Font(FONT_PRESS_START, 50)
fonte_big = pygame.font.Font(FONT_PRESS_START, 64)
texto_dire = "Escolha a direção!"

setas = [
    seta,
    pygame.transform.rotate(seta, 180),
    pygame.transform.rotate(seta, 90),
    pygame.transform.rotate(seta, -90)
]

DADO_SIZE = 96
dadobgs = [
    pygame.transform.smoothscale(pygame.image.load(p).convert_alpha(), (DADO_SIZE, DADO_SIZE))
    for p in UI_DICE
]

barras = [
    pygame.transform.smoothscale_by(
        pygame.image.load(get_asset_path("screens", "board", f"bar_{i}.png")).convert_alpha(), 0.25
    )
    for i in range(6)
]
barras_black = [utils.tint_mult(b, "black") for b in barras]

def casa_id_para_pos(tile_id):
    """Convert grid tile coordinates (x, y) to screen coordinates."""
    return (tile_id[0] * CASA_STRIDE + 8, tile_id[1] * CASA_STRIDE)

class Casa:
    """Represents an individual board tile."""
    def __init__(self, x, y, tipo, escolha=False):
        self.id = (x, y)
        self.pos = casa_id_para_pos(self.id)
        self.tipo = tipo
        self.escolha = escolha

Tile = Casa

class Tabuleiro:
    """Main board controller orchestrating turns, dice rolling, trivia cards, and camera view."""
    cam_pos = (0, 0)
    cam_movida = (0, 0)
    setas_mults = [0, 0, 0, 0]
    setas_direcoes = [-1, -1, -1, -1]
    escala_mapa = 1
    tabuleiro = None
    alphas = [0, 0, 0, 0]
    animacoes = [(None, 0, None) for _ in range(4)]

    def __init__(self, casas, jogo):
        self.modo = "dado"
        self.font_pergunta = pygame.font.Font(None, 56)
        self.font_resposta = pygame.font.Font(None, 48)
        self.font_dado = pygame.font.Font(None, 128)
        self.dado_numero = random.randint(1, 6)
        self.dado_tempo = 0
        self.tempo = 0
        self.pode_entrar_em_camera = False
        self.texto_dire = texto_dire
        self.hud_icons = {}
        self.dado_surfaces = {}
        self.carta_texto_cache = None
        self.carta_cache_key = None

        if casas is not None:
            self.casas = casas
        else:
            self.casas = []
            casa_inicial = None
            for y in range(len(MAPA)):
                for x in range(len(MAPA[0])):
                    if MAPA[y][x] == "X":
                        if casa_inicial is None:
                            casa_inicial = (x, y)
                        self.casas.append(Casa(x, y, random.choice(TIPOS)))
                    elif MAPA[y][x] == "M":
                        if casa_inicial is None:
                            casa_inicial = (x, y)
                        self.casas.append(Casa(x, y, "medalha"))
                    elif MAPA[y][x] == " ":
                        self.casas.append(Casa(x, y, "vazio"))

            for jogador in jogo.jogadores:
                jogador.casa = casa_inicial

    def encontrar_casa(self, tile_id):
        """Find non-empty tile at the given grid coordinates."""
        for casa in self.casas:
            if casa.id == tile_id and casa.tipo != "vazio":
                return casa
        return None

    def proxima_casa_e_direcao(self, jogador):
        """Determine next available tile and direction along player's trajectory."""
        direcoes = [
            (jogador.direcao[0], jogador.direcao[1]),
            (jogador.direcao[1], jogador.direcao[0]),
            (-jogador.direcao[1], -jogador.direcao[0]),
            (-jogador.direcao[0], -jogador.direcao[1])
        ]

        for direcao in direcoes:
            nova_casa = (jogador.casa[0] + direcao[0], jogador.casa[1] + direcao[1])
            casa = self.encontrar_casa(nova_casa)
            if casa is not None:
                return (nova_casa, direcao)
        return (jogador.casa, jogador.direcao)

    def animar(self, animacao, numero_jogador, param=None):
        """Trigger an animation state for a given player."""
        if self.animacoes[numero_jogador][0] != animacao or self.animacoes[numero_jogador][2] != param:
            self.animacoes[numero_jogador] = (animacao, pygame.time.get_ticks(), param)

    def outros_jogadores_em_casa(self, casa, jogo, exceto_numero):
        """Count other idle players currently residing on the same tile."""
        conta = 0
        for j in jogo.jogadores:
            if j.numero != exceto_numero and j.casa == casa and self.animacoes[j.numero][0] is None:
                conta += 1
        return conta

    def get_hud_icon(self, personagem):
        """Return cached scaled icon and its shadow tint for the player HUD."""
        if personagem not in self.hud_icons:
            ic = pygame.transform.smoothscale_by(utils.icones[personagem], 0.1)
            self.hud_icons[personagem] = (ic, utils.tint_mult(ic, "black"))
        return self.hud_icons[personagem]

    def get_dado_surfaces(self, numero):
        """Return cached rendered dice number surface and its shadow tint."""
        if numero not in self.dado_surfaces:
            txt = self.font_dado.render(str(numero), True, "black")
            shadow = utils.tint_mult(txt, (0, 0, 0, 31))
            self.dado_surfaces[numero] = (txt, shadow)
        return self.dado_surfaces[numero]

    def camerado(self, pos):
        """Transform world coordinate to camera-relative screen coordinate."""
        return (pos[0] - self.cam_pos[0] + 1066 / 2, pos[1] - self.cam_pos[1] + 600 / 2)

    def event(self, ev):
        if ev.type == pygame.MOUSEBUTTONDOWN or (
            ev.type == pygame.KEYDOWN and ev.key in [pygame.K_ESCAPE, pygame.K_RETURN, pygame.K_SPACE]
        ):
            if self.modo == "camera":
                self.modo = "dado"
            return True

    def frame(self, screen, delta, jogo):
        self.tempo += delta
        screen.fill(0xb4df5d)

        # Pre-render board background surface when size changes
        tabuleiro_size = (
            fundo.get_width() * CASA_STRIDE / 143 * screen.get_height() // 600,
            fundo.get_height() * CASA_STRIDE / 143 * screen.get_height() // 600
        )
        if self.tabuleiro is None or self.tabuleiro.get_size() != tabuleiro_size:
            self.tabuleiro = pygame.Surface(tabuleiro_size)
            h = fundo.get_height() * CASA_STRIDE / 143
            utils.smoothscaleblit(self.tabuleiro, h, fundo, (0, 0), None, CASA_STRIDE / 143)
            utils.smoothscaleblit(self.tabuleiro, h, objetos[0], (0, 0), None, CASA_STRIDE / 143)

            for casa in self.casas:
                if casa.id[0] == 0:
                    if casa.id[1] == 8:
                        utils.smoothscaleblit(self.tabuleiro, h, objetos[1], (0, 0), None, CASA_STRIDE / 143)
                    elif casa.id[1] == 12:
                        utils.smoothscaleblit(self.tabuleiro, h, objetos[2], (0, 0), None, CASA_STRIDE / 143)
                    elif casa.id[1] == 16:
                        utils.smoothscaleblit(self.tabuleiro, h, objetos[3], (0, 0), None, CASA_STRIDE / 143)
                    elif casa.id[1] == 17:
                        utils.smoothscaleblit(self.tabuleiro, h, objetos[4], (0, 0), None, CASA_STRIDE / 143)

                match casa.tipo:
                    case "teleporte":
                        utils.smoothscaleblit(self.tabuleiro, h, portal, casa.pos, None, CASA_SIZE / portal.get_height())
                    case "+R$5":
                        utils.smoothscaleblit(self.tabuleiro, h, cinero, casa.pos, None, CASA_SIZE / cinero.get_height())
                    case "-R$2":
                        utils.smoothscaleblit(self.tabuleiro, h, lixo, casa.pos, None, CASA_SIZE / lixo.get_height())
                    case "dado":
                        utils.smoothscaleblit(self.tabuleiro, h, dado, casa.pos, None, CASA_SIZE / dado.get_height())
                    case "minigame":
                        utils.smoothscaleblit(self.tabuleiro, h, minigame, casa.pos, None, CASA_SIZE / minigame.get_height())
                    case "medalha":
                        utils.smoothscaleblit(self.tabuleiro, h, medalha, casa.pos, None, CASA_SIZE / medalha.get_height())
                    case "carta":
                        utils.smoothscaleblit(self.tabuleiro, h, carta, casa.pos, None, CASA_SIZE / carta.get_height())
                    case "vazio":
                        pass

        if self.escala_mapa >= 1.249:
            utils.smoothscaleblit(screen, 600 * 1.25, self.tabuleiro, self.camerado((0, 0)), None, 600 / screen.get_height())
        elif abs(self.escala_mapa - 1.0) < 1e-4:
            escala_tela = screen.get_height() / 600
            cam = self.camerado((0, 0))
            screen.blit(self.tabuleiro, (cam[0] * escala_tela, cam[1] * escala_tela))
        else:
            utils.scaleblit(screen, 600 * self.escala_mapa, self.tabuleiro, self.camerado((0, 0)), None, 600 / screen.get_height())

        # Render and animate players
        tempo = pygame.time.get_ticks()
        jogador_atual_offset = (0, 0)
        render_order = [
            0 if jogo.jogador_atual > 0 else 1,
            1 if jogo.jogador_atual > 1 else 2,
            2 if jogo.jogador_atual > 2 else 3,
            jogo.jogador_atual
        ]

        for numero in render_order:
            if numero >= len(jogo.jogadores):
                continue
            jogador = jogo.jogadores[numero]
            outros_no_local = self.outros_jogadores_em_casa(jogador.casa, jogo, numero)
            pos = casa_id_para_pos(jogador.casa)
            animacao = self.animacoes[numero]
            sprite = jogador.get_andamento(jogador.direcao, True)

            match animacao:
                case ("andando", tempo_inicio, (pos_inicio, direcao)):
                    if tempo >= tempo_inicio + 500:
                        self.animar(None, numero)
                    sprite = jogador.get_andamento(direcao)
                    andado = (tempo - tempo_inicio) / 500 * CASA_STRIDE
                    pos = (pos_inicio[0] + andado * direcao[0], pos_inicio[1] + andado * direcao[1])
                    if jogador.numero == jogo.jogador_atual:
                        jogador_atual_offset = (andado * direcao[0], andado * direcao[1])
                case ("riqueza", tempo_inicio, _):
                    if tempo >= tempo_inicio + 1000:
                        jogo.passar_vez()
                        self.modo = "dado"
                        self.dado_numero = random.randint(1, 6)
                        self.animar(None, numero)
                    x = (tempo - tempo_inicio) / 250 * math.pi
                    if x % math.tau > math.pi:
                        x -= math.pi
                    pos = (pos[0], pos[1] - 24 * math.sin(x))
                    sprite = jogador.get_andamento("down", True)
                case ("robux", tempo_inicio, _):
                    if tempo >= tempo_inicio + 1000:
                        jogo.passar_vez()
                        self.modo = "dado"
                        self.dado_numero = random.randint(1, 6)
                        self.animar(None, numero)
                    t = (tempo - tempo_inicio) / 1000
                    t *= t
                    utils.smoothscaleblit(screen, 600, medalhas, self.camerado((pos[0] + 8, pos[1] - 32 - t * 72)), None, 0.4)
                case ("pobreza", tempo_inicio, _):
                    if tempo >= tempo_inicio + 1000:
                        jogo.passar_vez()
                        self.modo = "dado"
                        self.dado_numero = random.randint(1, 6)
                        self.animar(None, numero)
                    x = (tempo - tempo_inicio) / 250 * math.pi
                    if x % math.tau > math.pi:
                        x -= math.pi
                    t = 1 - math.sin(x)
                    sprite = utils.tint_mult(sprite, (255, 255 * t, 255 * t))
                case ("teleporte", tempo_inicio, _):
                    if tempo >= tempo_inicio + 1000:
                        jogador.casa = (random.randint(0, len(MAPA)), random.randint(0, len(MAPA[0])))
                        while not self.encontrar_casa(jogador.casa):
                            jogador.casa = (random.randint(0, len(MAPA)), random.randint(0, len(MAPA[0])))
                        jogo.passar_vez()
                        self.modo = "dado"
                        self.dado_numero = random.randint(1, 6)
                        self.animar(None, numero)
                    sprite = jogador.get_andamento(["down", "left", "up", "right"][(tempo - tempo_inicio) // 100 % 4], True)
                case ("carta", tempo_inicio, _):
                    utils.smoothscaleblit(screen, 600, interrogacao, self.camerado((pos[0] + 0, pos[1] + 0)))
                case ("decisao", tempo_inicio, _):
                    pass

            sprite_tamanho = (72, 78)
            if jogo.jogador_atual != numero:
                if self.alphas[numero] == 0:
                    self.alphas[numero] = 0.5
                else:
                    self.alphas[numero] = utils.lerp(self.alphas[numero], 0.5, 8 * delta)
            else:
                if self.alphas[numero] == 0:
                    self.alphas[numero] = 1
                else:
                    self.alphas[numero] = utils.lerp(self.alphas[numero], 1, 8 * delta)

            if jogo.jogador_atual != numero and outros_no_local > 0:
                match numero:
                    case 0:
                        pos = (pos[0] - 2, pos[1] + 4)
                    case 1:
                        pos = (pos[0] + 58, pos[1] + 4)
                    case 2:
                        pos = (pos[0] - 2, pos[1] + 52)
                    case 3:
                        pos = (pos[0] + 58, pos[1] + 52)
                sprite_tamanho = (24, 26)
            else:
                pos = (pos[0] + 6, pos[1] + 6)

            claridade = utils.clamp(255 * self.alphas[numero], 0, 255)
            pos = (pos[0] - 2, pos[1] - 8)
            utils.scaleblit(
                screen, 600 * self.escala_mapa,
                utils.tint_mult(pygame.transform.scale(sprite, sprite_tamanho), (claridade, claridade, claridade, 255)),
                self.camerado(pos)
            )

        # Process turn logic
        jogador = jogo.jogadores[jogo.jogador_atual]
        if self.modo == "dado":
            self.dado_tempo += delta
            if self.dado_tempo >= 0.1:
                self.dado_numero = random.randint(1, 6)
                self.dado_tempo = 0

        # Camera positioning
        proxima_cam_pos = casa_id_para_pos(jogo.jogadores[jogo.jogador_atual].casa)
        proxima_cam_pos = (proxima_cam_pos[0] + jogador_atual_offset[0] + 36, proxima_cam_pos[1] + jogador_atual_offset[1] + 36)
        if self.modo == "carta":
            proxima_cam_pos = (proxima_cam_pos[0] + 128, proxima_cam_pos[1])
        elif self.modo == "camera":
            self.escala_mapa = utils.lerp(self.escala_mapa, 1.25, 16 * delta)
            proxima_cam_pos = self.cam_movida
        else:
            self.escala_mapa = utils.lerp(self.escala_mapa, 1, 16 * delta)
            self.cam_movida = self.cam_pos

        if self.cam_pos == (0, 0):
            self.cam_pos = proxima_cam_pos
        else:
            speed = 16 if self.modo == "camera" else 4
            self.cam_pos = (
                utils.lerp(self.cam_pos[0], proxima_cam_pos[0], speed * delta),
                utils.lerp(self.cam_pos[1], proxima_cam_pos[1], speed * delta)
            )

        # Display HUD: player name, icon, coins, medals
        utils.smoothscaleblit(screen, 600, fonte.render(f"Jogador {jogo.jogador_atual + 1}", True, "black"), (4 + 2, 4 + 2), None, 0.5)
        utils.smoothscaleblit(screen, 600, fonte.render(f"Jogador {jogo.jogador_atual + 1}", True, PLAYER_BORDER_COLORS[jogo.jogador_atual]), (4, 4), None, 0.5)
        icon, icon_black = self.get_hud_icon(jogador.personagem)
        utils.smoothscaleblit(screen, 600, icon_black, (2, 47), None, 0.6)
        utils.smoothscaleblit(screen, 600, icon, (0, 45), None, 0.6)
        utils.smoothscaleblit(screen, 600, moedinha_black, (130, 96 + 2), None, 0.4)
        utils.smoothscaleblit(screen, 600, moedinha, (128, 96), None, 0.4)
        utils.smoothscaleblit(screen, 600, fonte_big.render(str(jogador.moedas), True, "black"), (180 + 2, 96 + 8 + 2), None, 0.5)
        utils.smoothscaleblit(screen, 600, fonte_big.render(str(jogador.moedas), True, "white"), (180 + 0, 96 + 8 + 0), None, 0.5)
        utils.smoothscaleblit(screen, 600, barras_black[jogador.medalhas], (6, 152), None, 0.5)
        utils.smoothscaleblit(screen, 600, barras[jogador.medalhas], (4, 150), None, 0.5)

        movimento = utils.movimento(1024, delta)
        if self.modo in ("andando", "dado"):
            dado_rect = pygame.Rect(0, 0, DADO_SIZE, DADO_SIZE)
            dado_rect.center = (screen.get_width() * 600 / screen.get_height() * 0.5, 600 * 0.75)
            utils.smoothscaleblit(screen, 600, dadobgs[jogo.jogador_atual], dado_rect.topleft)
            dado_texto, dado_texto_shadow = self.get_dado_surfaces(self.dado_numero)
            utils.smoothscaleblit(screen, 600, dado_texto, (dado_rect.x + 24, dado_rect.y + 8))
            utils.smoothscaleblit(screen, 600, dado_texto_shadow, (dado_rect.x + 25, dado_rect.y + 7))
            utils.smoothscaleblit(screen, 600, dado_texto_shadow, (dado_rect.x + 24, dado_rect.y + 6))
            utils.smoothscaleblit(screen, 600, dado_texto_shadow, (dado_rect.x + 23, dado_rect.y + 7))
            utils.smoothscaleblit(screen, 600, dado_texto_shadow, (dado_rect.x + 26, dado_rect.y + 8))
            utils.smoothscaleblit(screen, 600, dado_texto_shadow, (dado_rect.x + 22, dado_rect.y + 8))
            utils.smoothscaleblit(screen, 600, dado_texto_shadow, (dado_rect.x + 25, dado_rect.y + 9))
            utils.smoothscaleblit(screen, 600, dado_texto_shadow, (dado_rect.x + 24, dado_rect.y + 10))
            utils.smoothscaleblit(screen, 600, dado_texto_shadow, (dado_rect.x + 23, dado_rect.y + 9))
        elif self.modo == "carta":
            tempo_inicio = self.animacoes[jogador.numero][1]
            vw = screen.get_width() * 600 / screen.get_height()
            carta_escala = 0.4
            cartabgw = cartabg.get_width() * carta_escala
            cartabgh = cartabg.get_height() * carta_escala
            tempo_anim = tempo - tempo_inicio
            t = utils.clamp(tempo_anim / 200, 0, 1)
            t *= t
            screen.fill((255 - t * 127, 255 - t * 127, 255 - t * 127), None, pygame.BLEND_MULT)
            carta_pos = (vw * 2 / 3 - cartabgw / 2, utils.lerp(600, 300 - cartabgh * 0.5, t))
            utils.smoothscaleblit(screen, 600, cartabg, carta_pos, None, carta_escala)
            utils.smoothscaleblit(screen, 600, cartabg, (carta_pos[0] + 24, carta_pos[1] + 24), None, 0.25)
            utils.smoothscaleblit(screen, 600, cartabg, carta_pos, None, carta_escala)

            pergunta = perguntas.get_pergunta()
            escala_tela = screen.get_height() / 600

            # Render dynamic backgrounds for answer options (hover, correct, wrong)
            pgt_y = carta_pos[1] + cartabgh * 0.5 + 24
            pgt_h = 56
            resposta = perguntas.get_resposta()
            for i in range(4):
                if resposta == i or resposta is None or (resposta is not None and pergunta[5] == i):
                    alt_fundo_rect = pygame.Rect(carta_pos[0] + 53 * carta_escala, pgt_y - 4, 737 * carta_escala, pgt_h)
                    if resposta is not None and pergunta[5] == i:
                        utils.scaledrawrect(screen, 600, 0x0fbb1e, alt_fundo_rect)
                    elif resposta == i:
                        utils.scaledrawrect(screen, 600, 0xbb0f1e, alt_fundo_rect)
                    elif alt_fundo_rect.collidepoint(utils.mouse_pos_para(screen, 600)):
                        utils.scaledrawrect(screen, 600, 0x550f1e, alt_fundo_rect)
                        if pygame.mouse.get_pressed()[0]:
                            perguntas.escolher_resposta(i)
                pgt_y += pgt_h

            # Check / update cached static text surface for the card
            cache_key = (perguntas.get_versao(), screen.get_size())
            if self.carta_texto_cache is None or self.carta_cache_key != cache_key:
                card_surf_w = int(round(cartabgw * escala_tela))
                card_surf_h = int(round(cartabgh * escala_tela))
                card_text_surf = pygame.Surface((card_surf_w, card_surf_h), pygame.SRCALPHA)

                # Question text
                q_rect = pygame.Rect(40, 96, cartabgw - 80, 0)
                utils.smoothscale_draw_text(card_text_surf, cartabgh, pergunta[0], "white", q_rect, self.font_pergunta, 0.5, sombra=True)

                # Answers text
                opt_rect = pygame.Rect(72, cartabgh * 0.5 + 24, cartabgw - 112, 56)
                for i in range(4):
                    utils.smoothscale_draw_text(card_text_surf, cartabgh, ["A)", "B)", "C)", "D)"][i], "white", opt_rect.move(-24, 0), self.font_resposta, 0.5, sombra=True)
                    utils.smoothscale_draw_text(card_text_surf, cartabgh, pergunta[i + 1], "white", opt_rect, self.font_resposta, 0.5, sombra=True)
                    opt_rect.y += 56

                self.carta_texto_cache = card_text_surf
                self.carta_cache_key = cache_key

            # Blit the pre-rendered text surface directly over the card
            screen.blit(self.carta_texto_cache, (carta_pos[0] * escala_tela, carta_pos[1] * escala_tela))
        elif self.modo == "camera":
            self.setas_mults = [
                utils.clamp(self.setas_mults[0] + self.setas_direcoes[0] * 4 * delta, -1.0, 2.0),
                utils.clamp(self.setas_mults[1] + self.setas_direcoes[1] * 4 * delta, -1.0, 2.0),
                utils.clamp(self.setas_mults[2] + self.setas_direcoes[2] * 4 * delta, -1.0, 2.0),
                utils.clamp(self.setas_mults[3] + self.setas_direcoes[3] * 4 * delta, -1.0, 2.0)
            ]
            movendo = [movimento[1] < 0, movimento[1] > 0, movimento[0] < 0, movimento[0] > 0]
            for i in range(4):
                if self.setas_mults[i] > 1.0:
                    self.setas_direcoes[i] = -1
                    self.setas_mults[i] = 2.0 - self.setas_mults[i]
                elif self.setas_mults[i] < 0.0:
                    if movendo[i]:
                        self.setas_direcoes[i] = 1
                        self.setas_mults[i] = -self.setas_mults[i]
                    else:
                        self.setas_mults[i] = 0.0
                elif movendo[i] and self.setas_direcoes[i] == 0 and self.setas_mults[i] == 0.0:
                    self.setas_direcoes[i] = 1
            utils.smoothscaleblit(screen, 600, setas[0], (screen.get_width() * 600 / screen.get_height() / 2 - 32, (1 - self.setas_mults[0]) * 8), None, 0.25)
            utils.smoothscaleblit(screen, 600, setas[1], (screen.get_width() * 600 / screen.get_height() / 2 - 32, 600 - 64 - (1 - self.setas_mults[1]) * 8), None, 0.25)
            utils.smoothscaleblit(screen, 600, setas[2], ((1 - self.setas_mults[2]) * 8, 300 - 32), None, 0.25)
            utils.smoothscaleblit(screen, 600, setas[3], (screen.get_width() * 600 / screen.get_height() - 64 - (1 - self.setas_mults[3]) * 8, 300 - 32), None, 0.25)

        # Process movement steps
        if self.modo == "andando":
            self.dado_tempo += delta
            if self.dado_tempo >= 0.5:
                if self.dado_numero == 0:
                    casa = self.encontrar_casa(jogador.casa)
                    match casa.tipo:
                        case "minigame":
                            if self.dado_tempo >= 1:
                                return "minigame"
                        case "carta":
                            self.modo = "carta"
                            self.animar("carta", jogador.numero)
                            perguntas.reescolher_pergunta()
                        case "dado":
                            if self.dado_tempo >= 1:
                                self.modo = "dado"
                                self.dado_numero = random.randint(1, 6)
                                self.dado_tempo = 0
                            self.animar(None, jogador.numero)
                        case "+R$5":
                            self.animar("riqueza", jogador.numero)
                            jogo.receber_moedas(3)
                            self.modo = "animando"
                            self.dado_tempo = 0
                        case "-R$2":
                            self.animar("pobreza", jogador.numero)
                            jogo.perder_moedas(3)
                            self.modo = "animando"
                            self.dado_tempo = 0
                        case "teleporte":
                            self.animar("teleporte", jogador.numero)
                            self.modo = "animando"
                            self.dado_tempo = 0
                        case "medalha":
                            if jogador.moedas >= 30:
                                self.animar("robux", jogador.numero)
                                self.modo = "animando"
                                jogo.perder_moedas(30)
                                jogador.medalhas += 1
                                if jogador.medalhas >= 5:
                                    return "venceu"
                                elif self.dado_tempo >= 1:
                                    self.modo = "dado"
                                    self.dado_numero = random.randint(1, 6)
                                    self.dado_tempo = 0
                            else:
                                self.animar("pobreza", jogador.numero)
                                self.modo = "animando"
                                if self.dado_tempo >= 1:
                                    self.modo = "dado"
                                    self.dado_numero = random.randint(1, 6)
                                    self.dado_tempo = 0
                        case "decisao":
                            self.animar("riqueza", jogador.numero)
                            self.modo = "animando"
                            self.dado_tempo = 0
                else:
                    self.dado_numero -= 1
                    if self.dado_numero > 0:
                        self.dado_tempo = 0
                    (casa, direcao) = self.proxima_casa_e_direcao(jogador)
                    jogador.casa = casa
                    jogador.direcao = direcao
                    if self.encontrar_casa(jogador.casa).tipo in ("medalha", "decisao"):
                        self.dado_numero = 0
                        self.dado_tempo = 0
            if self.dado_tempo < 0.5 and self.dado_numero > 0:
                (casa, direcao) = self.proxima_casa_e_direcao(jogador)
                self.animar("andando", jogador.numero, (casa_id_para_pos(jogador.casa), direcao))

        if self.modo not in ("andando", "animando"):
            self.animar(None, 0)
            self.animar(None, 1)
            self.animar(None, 2)
            self.animar(None, 3)

        match self.modo:
            case "dado":
                if utils.pressionado_agora[pygame.K_SPACE] or utils.pressionado_agora[pygame.K_RETURN]:
                    self.dado_tempo = 0
                    self.modo = "andando"
                elif movimento[0] != 0 or movimento[1] != 0:
                    if self.pode_entrar_em_camera:
                        self.modo = "camera"
                else:
                    self.pode_entrar_em_camera = True
            case "carta":
                if perguntas.get_resposta() is not None:
                    if perguntas.get_tempo_apos_escolha() >= 1000:
                        if perguntas.get_resposta() == perguntas.get_pergunta()[5]:
                            jogo.receber_moedas(10)
                            self.animar("riqueza", jogador.numero)
                            self.modo = "animando"
                        else:
                            jogo.passar_vez()
                            self.modo = "dado"
                            self.dado_tempo = 0
                            self.dado_numero = random.randint(1, 6)
                            self.animar(None, jogador.numero)
            case "camera":
                virtual_width = screen.get_width() * 600 / screen.get_height()
                self.cam_movida = (
                    utils.clamp(self.cam_movida[0] + movimento[0], 1066 / 2, fundo.get_width() - 1960 * virtual_width / 1066),
                    utils.clamp(self.cam_movida[1] + movimento[1], 600 / 2, fundo.get_height() - 1620)
                )

BoardScreen = Tabuleiro
