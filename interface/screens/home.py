import pygame

from interface.components.button import Button
from interface.drawing.centered_text import centered_text
from interface.components.chess_decoration import chess_decoration

HOME_BUTTONS = [
    Button(pygame.Rect(250, 360, 300, 52), 'Jogar', 'modes', primary=True),
    Button(pygame.Rect(250, 428, 300, 52), 'Regras', 'rules'),
]

def draw_home(surface):
    centered_text(surface, 'Xadrez', 85, 42, bold=True)
    decoration = chess_decoration()
    surface.blit(decoration, decoration.get_rect(midtop=(surface.get_width() // 2, 145)))
