import pygame

from interface.components.button import Button
from interface.components.draw_board import draw_board
from interface.drawing.font import font
from interface.theme import PANEL, TEXT
from src.domain.color import Color

HINTS_BUTTON = Button(pygame.Rect(576, 34, 104, 28), 'Dicas', is_toggle=True, checked=True)
MULTIPLAYER_BUTTONS = [
    Button(pygame.Rect(32, 24, 48, 48), 'Voltar', 'modes', icon='arrow-left.png'),
    Button(pygame.Rect(720, 24, 48, 48), 'Regras', 'rules', icon='book-2.png'),
    HINTS_BUTTON,
]


AI_BUTTONS = [
    Button(pygame.Rect(32, 24, 48, 48), 'Voltar', 'ai_levels', icon='arrow-left.png'),
    Button(pygame.Rect(720, 24, 48, 48), 'Regras', 'rules', icon='book-2.png'),
    HINTS_BUTTON,
]


def draw_multiplayer(surface, game, title='Multiplayer', animation=None):
    draw_board(surface, game, HINTS_BUTTON.checked, animation)
    surface.blit(font(28, True).render(title, True, TEXT), (100, 30))
    pygame.draw.rect(surface, PANEL, (32, 542, 736, 42), border_radius=12)
    turn = 'Brancas' if game.current_turn is Color.WHITE else 'Pretas'
    surface.blit(font(18, True).render(f'Turno: {turn}', True, TEXT), (48, 553))
    if game.status_message != f'Turno: {turn}':
        message = font(16).render(game.status_message, True, TEXT)
        surface.blit(message, (240, 554))
