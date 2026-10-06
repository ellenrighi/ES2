import pygame

from interface.components.button import Button
from interface.components.draw_button import draw_button
from interface.drawing.font import font
from interface.theme import PANEL, TEXT

PROMOTION_OPTIONS = [
    (code, Button(pygame.Rect(150 + index * 128, 298, 116, 48), label))
    for index, (code, label) in enumerate([
        ('Q', 'Dama (Q)'), ('R', 'Torre (R)'),
        ('B', 'Bispo (B)'), ('N', 'Cavalo (N)'),
    ])
]


def draw_promotion_popup(surface):
    overlay = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 155))
    surface.blit(overlay, (0, 0))
    pygame.draw.rect(surface, PANEL, (128, 224, 544, 146), border_radius=18)
    title = font(24, True).render('Escolha a promoção do peão', True, TEXT)
    surface.blit(title, title.get_rect(center=(400, 260)))
    for _, button in PROMOTION_OPTIONS:
        draw_button(button, surface, (-1, -1), False)
