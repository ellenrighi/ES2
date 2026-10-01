import random

from src.domain.color import Color


def get_all_moves(board, color): 
    moves = []

    for row in range(8):
        for col in range(8):
            piece = board.get_piece(row, col)

            if piece is not None and piece.color is color:
                piece_moves = board.generate_moves_for_piece(row, col)
                moves.extend(piece_moves)

    return moves


def choose_random_move(board, color): 
    moves = get_all_moves(board, color)

    if not moves:
        return None

    return random.choice(moves)