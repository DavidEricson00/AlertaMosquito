"""Utility functions for rendering, scaling, text wrapping, physics and collision detection."""

import pygame
import math
from src.core.paths import CHARACTER_WALK_SPRITES, CHARACTER_ICONS

# Global input states used across frames
pressionado = pygame.key.get_pressed()
pressionado_agora = pressionado
mouse_pos = (0, 0)

def mouse_pos_para(screen, altura_esperada):
    """Transform global mouse coordinates relative to expected screen height."""
    escala = altura_esperada / screen.get_height()
    return (mouse_pos[0] * escala, mouse_pos[1] * escala)

# Preloaded character walk animation frames and icons
andamentos = [
    pygame.image.load(path) for path in CHARACTER_WALK_SPRITES
]

icones = [
    pygame.image.load(path) for path in CHARACTER_ICONS
]

def clamp(v, x, y):
    """Clamp value v between bounds x and y."""
    return max(min(v, y), x)

cache_anterior = {}
cache_atual = {}

def clear_cache():
    """Cycle the scaled surface caches between frames."""
    global cache_anterior, cache_atual
    cache_anterior.clear()
    cache_anterior = cache_atual
    cache_atual = {}

def scaledrawrect(screen, altura_esperada, color, rect, border_radius=-1):
    """Draw a rectangle scaled according to the screen height relative to expected height."""
    escala = screen.get_height() / altura_esperada
    pygame.draw.rect(
        screen,
        color,
        (rect[0] * escala, rect[1] * escala, rect[2] * escala, rect[3] * escala),
        border_radius=border_radius
    )

def scaleblit(screen, altura_esperada, obj, pos, area=None, escala_extra=1):
    """Blit a surface with nearest-neighbor scaling."""
    escala_tela = screen.get_height() / altura_esperada
    escala_total = escala_tela * escala_extra

    if area is None:
        area = obj.get_rect()
    else:
        area = pygame.Rect(area)

    if abs(escala_total - 1.0) < 1e-4:
        sub = obj if area == obj.get_rect() else obj.subsurface(area)
        screen.blit(sub, (pos[0] * escala_tela, pos[1] * escala_tela))
        return

    escalado = pygame.transform.scale_by(obj.subsurface(area), escala_total)
    screen.blit(escalado, (pos[0] * escala_tela, pos[1] * escala_tela))

def smoothscaleblit(screen, altura_esperada, obj, pos, area=None, escala_extra=1, fake=False):
    """Blit a surface using smooth scaling with caching to optimize performance."""
    escala_tela = screen.get_height() / altura_esperada
    escala_total = escala_tela * escala_extra

    if area is None:
        area = obj.get_rect()
    else:
        area = pygame.Rect(area)

    if abs(escala_total - 1.0) < 1e-4:
        escalado = obj if area == obj.get_rect() else obj.subsurface(area)
    else:
        key = (obj, area[0], area[1], area[2], area[3], escala_total)
        escalado = cache_atual.get(key)
        if escalado is None:
            escalado = cache_anterior.get(key)
            if escalado is None:
                escalado = pygame.transform.smoothscale_by(obj.subsurface(area), escala_total)
            cache_atual[key] = escalado
    if not fake:
        screen.blit(escalado, (pos[0] * escala_tela, pos[1] * escala_tela))

def tint_mult(obj, cor):
    """Apply a multiplicative color tint to an image."""
    if cor not in ((255, 255, 255, 255), (255, 255, 255), "white"):
        obj = obj.copy()
        obj.fill(cor, None, pygame.BLEND_RGBA_MULT)
    return obj

def blitanimado(screen, obj, pos, tempo, fps):
    """Blit a frame from an animated sequence of surfaces."""
    frame_atual = int(tempo * fps) % len(obj)
    screen.blit(obj[frame_atual], pos)

def lerp(x, y, t):
    """Linear interpolation between x and y with factor t."""
    return x + (y - x) * clamp(t, 0, 1)

def imagem_colide_com_rect(rect, obj, pos):
    """Check collision between a rectangle and a positioned surface bounding box."""
    return rect.colliderect(obj.get_rect().move(pos[0], pos[1]))

def colide_com_imagem(img, obj, pos):
    """Check pixel transparency collision at corners of obj against img."""
    return (
        img.get_at((int(pos[0]), int(pos[1])))[3] != 0
        or img.get_at((int(pos[0]) + obj.get_width(), int(pos[1])))[3] != 0
        or img.get_at((int(pos[0]), int(pos[1]) + obj.get_height()))[3] != 0
        or img.get_at((int(pos[0]) + obj.get_width(), int(pos[1]) + obj.get_height()))[3] != 0
    )

def movimento(pixelsporsegundo, delta):
    """Calculate 2D movement vector based on WASD or arrow keys input."""
    move_x = 0
    move_y = 0
    if pressionado[pygame.K_w] or pressionado[pygame.K_UP]:
        move_y -= 1
    if pressionado[pygame.K_s] or pressionado[pygame.K_DOWN]:
        move_y += 1
    if pressionado[pygame.K_a] or pressionado[pygame.K_LEFT]:
        move_x -= 1
    if pressionado[pygame.K_d] or pressionado[pygame.K_RIGHT]:
        move_x += 1
    length = math.sqrt(move_x * move_x + move_y * move_y)
    if length > 1:
        move_x /= length
        move_y /= length
    return (move_x * pixelsporsegundo * delta, move_y * pixelsporsegundo * delta)

def deslize(img, obj, pos, movimento_vetor):
    """Attempt 2D movement against an obstacle image with sliding along axes."""
    destino = (pos[0] + movimento_vetor[0], pos[1] + movimento_vetor[1])
    if colide_com_imagem(img, obj, destino):
        destino = (pos[0] + movimento_vetor[0], pos[1])
        if colide_com_imagem(img, obj, destino):
            destino = (pos[0], pos[1] + movimento_vetor[1])
            if colide_com_imagem(img, obj, destino):
                return pos
    return destino

def smoothscale_draw_text(surface, altura_esperada, text, color, rect, font, escala=1, aa=True, bkg=None, sombra=False):
    """Draw text wrapped into an area with smooth scaling and optional shadow."""
    rect = pygame.Rect(rect)
    y = rect.top
    line_spacing = -2
    font_height = font.size("Tg")[1] * escala
    max_width = rect.width / escala

    shadow_offsets = [
        (-1, -1), (-2, 0), (-1, 1),
        (0, -2), (0, 0), (0, 2),
        (1, -1), (2, 0), (1, 1)
    ] if sombra else None

    while text:
        i = 1
        while font.size(text[:i])[0] < max_width and i < len(text):
            i += 1

        if i < len(text):
            sp = text.rfind(" ", 0, i)
            if sp != -1:
                i = sp + 1

        line = text[:i]

        if shadow_offsets:
            shadow_img = font.render(line, aa, (0, 0, 0, 63))
            for dx, dy in shadow_offsets:
                smoothscaleblit(surface, altura_esperada, shadow_img, (rect.left + dx, y + dy), None, escala)

        if bkg:
            image = font.render(line, 1, color, bkg)
            image.set_colorkey(bkg)
        else:
            image = font.render(line, aa, color)

        smoothscaleblit(surface, altura_esperada, image, (rect.left, y), None, escala)
        y += font_height + line_spacing

        text = text[i:]
        if i == 0:
            break

    return text
