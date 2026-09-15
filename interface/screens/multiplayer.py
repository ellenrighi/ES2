import pygame

from interface.components.button import Button
from interface.components.draw_board import draw_board
from interface.drawing.font import font
from interface.theme import PANEL, TEXT

HINTS_BUTTON = Button(pygame.Rect(576, 34, 104, 28), 'Dicas', enabled=False, is_toggle=True)
MULTIPLAYER_BUTTONS = [
    Button(pygame.Rect(32, 24, 48, 48), 'Voltar', 'modes', icon='arrow-left.png'),
    Button(pygame.Rect(720, 24, 48, 48), 'Regras', 'rules', icon='book-2.png'),
    HINTS_BUTTON,
]


def draw_multiplayer(surface):
    draw_board(surface)
    surface.blit(font(28, True).render('Multiplayer', True, TEXT), (100, 30))
    pygame.draw.rect(surface, PANEL, (32, 542, 736, 42), border_radius=12)
