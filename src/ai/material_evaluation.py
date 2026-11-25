from src.domain.color import Color
from src.domain.piece import Pawn, Knight, Bishop, Rook, Queen


PIECE_VALUES = {
    Pawn: 1,
    Knight: 3,
    Bishop: 3,
    Rook: 5,
    Queen: 9,
}


def evaluate_material(board, color: Color) -> int:
    # Calcula a diferenca de material entre uma cor e o adversario.
    score = 0

    for row in range(8):
        for col in range(8):
            piece = board.get_piece(row, col)

            if piece is None:
                continue

            value = PIECE_VALUES.get(type(piece), 0)

            if piece.color is color:
                score += value
            else:
                score -= value

    return score