import pygame

from interface.components.draw_piece import draw_piece
from interface.theme import PANEL

BOARD = pygame.Rect(192, 96, 416, 416)
SQUARE_SIZE = 52
BACK_RANK = ('rook', 'knight', 'bishop', 'queen', 'king', 'bishop', 'knight', 'rook')


def draw_board(surface):
    """Desenha a posição inicial; as peças ainda não são interativas."""
    pygame.draw.rect(surface, PANEL, BOARD.inflate(20, 20), border_radius=12)
    for row in range(8):
        for column in range(8):
            square = pygame.Rect(BOARD.x + column * SQUARE_SIZE,
                                 BOARD.y + row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
            color = '#ACB99A' if (row + column) % 2 == 0 else '#526B54'
            pygame.draw.rect(surface, color, square)
            if row in (0, 7):
                draw_piece(surface, BACK_RANK[column], 'black' if row == 0 else 'white', square.center)
            elif row in (1, 6):
                draw_piece(surface, 'pawn', 'black' if row == 1 else 'white', square.center)
