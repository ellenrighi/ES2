from src.domain.color import Color


CENTER_SQUARES = {
    (3, 3),
    (3, 4),
    (4, 3),
    (4, 4),
}


def evaluate_position(board, color: Color) -> int:
    # Da uma pontuacao extra para pecas que ocupam o centro do tabuleiro.
    score = 0

    for row in range(8):
        for col in range(8):
            piece = board.get_piece(row, col)

            if piece is None:
                continue

            if (row, col) in CENTER_SQUARES:
                if piece.color is color:
                    score += 1
                else:
                    score -= 1

    return score