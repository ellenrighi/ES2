import pygame

from interface.components.draw_toggle import draw_toggle
from interface.drawing.font import font
from interface.drawing.load_icon import load_icon
from interface.theme import ACCENT, BACKGROUND, MUTED, PANEL, TEXT


def draw_button(button, surface, mouse, focused):
    hovered = button.enabled and button.rect.collidepoint(mouse)
    now = pygame.time.get_ticks()
    elapsed = min(now - button.hover_updated_at, 50) if button.hover_updated_at else 0
    button.hover_updated_at = now
    step = elapsed / 160
    if not button.enabled:
        button.hover_progress = 0
    elif hovered:
        button.hover_progress = min(1, button.hover_progress + step)
    else:
        button.hover_progress = max(0, button.hover_progress - step)
    progress = button.hover_progress

    if button.is_toggle:
        draw_toggle(button, surface, focused, step)
        return

    if not button.enabled:
        background, foreground = '#29332D', MUTED
    elif button.primary:
        background = pygame.Color(ACCENT).lerp('#E8C989', progress)
        foreground = pygame.Color(BACKGROUND).lerp('#080D09', progress)
    else:
        background = pygame.Color(PANEL).lerp('#36453A', progress)
        foreground = pygame.Color(TEXT).lerp(ACCENT, progress)

    rect = button.rect
    if progress > 0:
        shadow = pygame.Surface((rect.width + 24, rect.height + 30), pygame.SRCALPHA)
        for blur in range(10, 0, -2):
            bounds = pygame.Rect(12, 18, rect.width, rect.height).inflate(blur * 2, blur * 2)
            pygame.draw.rect(shadow, (0, 0, 0, round((12 - blur) * 8 * progress)),
                             bounds, border_radius=12 + blur)
        surface.blit(shadow, (rect.x - 12, rect.y - 12))

    pygame.draw.rect(surface, background, rect, border_radius=12)
    if progress > 0:
        border = pygame.Color(background).lerp('#F8DEAC' if button.primary else ACCENT, progress)
        pygame.draw.rect(surface, border, rect, 1, 12)
    if focused and button.enabled:
        pygame.draw.rect(surface, TEXT, rect.inflate(8, 8), 2, 15)
    label = load_icon(button.icon) if button.icon else font(19, True).render(button.label, True, foreground)
    if progress > 0:
        scale = 1 + 0.08 * progress
        label = pygame.transform.smoothscale(label, (round(label.get_width() * scale),
                                                    round(label.get_height() * scale)))
    surface.blit(label, label.get_rect(center=rect.center))
