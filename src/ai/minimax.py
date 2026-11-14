from src.domain.color import Color
from src.ai.board_evaluation import evaluate_board


def expand_node(board, color: Color):
    # Gera todos os estados possiveis a partir das jogadas legais.
    return board.generate_successors(color)


def minimax(board, depth: int, maximizing: bool, ai_color: Color) -> int:
    # Quando chega na profundidade definida, avalia o tabuleiro.
    if depth == 0:
        return evaluate_board(board, ai_color)

    # Escolhe a cor que deve jogar neste nivel da arvore.
    current_color = ai_color if maximizing else ai_color.opposite()

    # Expande o no atual gerando os proximos estados.
    successors = expand_node(board, current_color)

    # Se nao houver movimentos, avalia o estado atual.
    if not successors:
        return evaluate_board(board, ai_color)

    if maximizing:
        best_value = float("-inf")

        for _, new_board in successors:
            value = minimax(
                new_board,
                depth - 1,
                False,
                ai_color
            )

            best_value = max(best_value, value)

        return best_value

    best_value = float("inf")

    for _, new_board in successors:
        value = minimax(
            new_board,
            depth - 1,
            True,
            ai_color
        )

        best_value = min(best_value, value)

    return best_value