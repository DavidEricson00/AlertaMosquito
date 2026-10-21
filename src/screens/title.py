"""Title screen with game logo and start prompt."""

import pygame
import src.core.utils as utils
from src.core.paths import get_asset_path, FONT_MILKS

fonte = pygame.font.Font(FONT_MILKS, 30)
fonte1 = pygame.font.Font(FONT_MILKS, 25)

class Titulo:
    """Title screen controller managing intro logo animations and start inputs."""
    def __init__(self):
        self.logo = pygame.image.load(get_asset_path("screens", "title", "logo.png")).convert_alpha()
        self.bg = pygame.image.load(get_asset_path("screens", "title", "background.png")).convert_alpha()
        self.comecar = False

    def event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in [
                pygame.K_KP_ENTER, pygame.K_RETURN, pygame.K_SPACE,
                pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_m
            ]:
                self.comecar = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            self.comecar = True

    def frame(self, screen, delta, jogo):
        # Draw background
        screen.blit(pygame.transform.smoothscale(self.bg, screen.get_size()), (0, 0))

        # Calculate proportional logo scaling
        max_logo_width = screen.get_width() * 0.9
        max_logo_height = screen.get_height() * 0.9

        logo_rect = self.logo.get_rect()
        logo_scaled_rect = logo_rect.scale_by(max_logo_height / logo_rect.height)
        if logo_scaled_rect.width > max_logo_width:
            logo_scaled_rect = logo_rect.scale_by(max_logo_width / logo_rect.width)

        logo_scaled = pygame.transform.smoothscale_by(self.logo, logo_scaled_rect.height / self.logo.get_height())
        logo_rect = logo_scaled.get_rect(center=screen.get_rect().center)
        logo_rect.centery = screen.get_rect().centery - screen.get_height() // 15
        screen.blit(logo_scaled, logo_rect)

        # Draw instructional messages
        mensagem = 'Pressione qualquer tecla para iniciar'
        mensagem1 = 'Pressione esc para sair'
        texto_formatado = fonte.render(mensagem, True, (255, 255, 255))
        texto_formatado1 = fonte1.render(mensagem1, True, (255, 255, 255))
        utils.scaleblit(screen, 600, texto_formatado, (600 / screen.get_height() * screen.get_width() / 2 - texto_formatado.get_width() / 2, 480))
        utils.scaleblit(screen, 600, texto_formatado1, (600 / screen.get_height() * screen.get_width() / 2 - texto_formatado1.get_width() / 2, 530))

        # Selection verification and hotkeys
        if self.comecar:
            if utils.pressionado_agora[pygame.K_1]:
                return "minigame0"
            elif utils.pressionado_agora[pygame.K_2]:
                return "minigame1"
            elif utils.pressionado_agora[pygame.K_3]:
                return "minigame2"
            elif utils.pressionado_agora[pygame.K_4]:
                return "minigame3"
            elif utils.pressionado_agora[pygame.K_m]:
                return "minigame"
            else:
                return "selecion"

TitleScreen = Titulo
