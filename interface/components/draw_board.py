import pygame

from interface.components.draw_piece import draw_piece
from interface.theme import ACCENT, PANEL
from src.domain.color import Color

BOARD = pygame.Rect(192, 96, 416, 416)
SQUARE_SIZE = 52


def draw_board(surface, game, show_hints=True, animation=None):
    """Desenha as peças e a seleção a partir do estado da partida."""
    animating = animation is not None and animation.active
    board = animation.board if animating else game.board
    moving = animation.moving_pieces() if animating else []
    origins = {start for start, end in moving}
    pygame.draw.rect(surface, PANEL, BOARD.inflate(20, 20), border_radius=12)
    for row in range(8):
        for column in range(8):
            square = pygame.Rect(BOARD.x + column * SQUARE_SIZE,
                                 BOARD.y + row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
            color = '#ACB99A' if (row + column) % 2 == 0 else '#526B54'
            pygame.draw.rect(surface, color, square)
            piece = board.get_piece(row, column)
            if piece is not None and (row, column) not in origins:
                side = 'white' if piece.color is Color.WHITE else 'black'
                draw_piece(surface, type(piece).__name__.lower(), side, square.center)
            if game.selected_square == (row, column):
                pygame.draw.rect(surface, ACCENT, square.inflate(-4, -4), 3)
            if show_hints and (row, column) in game.legal_moves_by_dest:
                if piece is None:
                    pygame.draw.circle(surface, ACCENT, square.center, 6)
                else:
                    pygame.draw.rect(surface, ACCENT, square.inflate(-4, -4), 3)
    if animating:
        progress = animation.elapsed_ms / animation.DURATION_MS
        progress = progress * progress * (3 - 2 * progress)
        for start, end in moving:
            piece = board.get_piece(*start)
            x = BOARD.x + (start[1] + (end[1] - start[1]) * progress + 0.5) * SQUARE_SIZE
            y = BOARD.y + (start[0] + (end[0] - start[0]) * progress + 0.5) * SQUARE_SIZE
            side = 'white' if piece.color is Color.WHITE else 'black'
            draw_piece(surface, type(piece).__name__.lower(), side, (round(x), round(y)))
