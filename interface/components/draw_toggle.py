import pygame

from interface.drawing.font import font
from interface.theme import ACCENT, BACKGROUND, MUTED, TEXT


def draw_toggle(button, surface, focused, step):
    if not button.enabled:
        button.toggle_progress = 0
    elif button.checked:
        button.toggle_progress = min(1, button.toggle_progress + step)
    else:
        button.toggle_progress = max(0, button.toggle_progress - step)
    progress = button.toggle_progress
    track = pygame.Rect(button.rect.x, button.rect.y + 2, 44, 24)
    color = pygame.Color('#46554B').lerp(ACCENT, progress) if button.enabled else '#344039'
    pygame.draw.rect(surface, color, track, border_radius=15)
    knob_x = track.x + 12 + round(20 * progress)
    knob_color = (BACKGROUND if button.checked else TEXT) if button.enabled else MUTED
    pygame.draw.circle(surface, knob_color, (knob_x, track.centery), 8)
    label = font(20, True).render(button.label, True, TEXT if button.enabled else MUTED)
    surface.blit(label, label.get_rect(midleft=(track.right + 8, track.centery)))
    if button.enabled and (focused or button.hover_progress > 0):
        pygame.draw.rect(surface, ACCENT if focused else MUTED,
                         track.inflate(6, 6), 1, 18)
