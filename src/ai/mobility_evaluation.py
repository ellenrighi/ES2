from src.domain.color import Color


def evaluate_mobility(board, color: Color) -> int:
    # Compara quantos movimentos legais cada lado possui.
    own_moves = 0
    opponent_moves = 0

    for row in range(8):
        for col in range(8):
            piece = board.get_piece(row, col)

            if piece is None:
                continue

            moves = board.generate_moves_for_piece(row, col)

            if piece.color is color:
                own_moves += len(moves)
            else:
                opponent_moves += len(moves)

    return own_moves - opponent_moves