import time

from src.domain.color import Color
from src.ai.board_evaluation import evaluate_board
from src.ai.material_evaluation import PIECE_VALUES


SEARCH_TIME_LIMIT_SECONDS = 10.0


class SearchTimeout(Exception):
    pass


def expand_node(board, color: Color):
    # Gera e ordena capturas antes dos movimentos sem captura. Antecipa o momento de poda alfa-beta, priorizando movimentos que capturam peças mais valiosas.
    successors = board.generate_successors(color)
    return sorted(
        successors,
        key=lambda successor: _move_order_score(board, successor[0]),
        reverse=True,
    )


def _move_order_score(board, move) -> int:
    # Retorna uma pontuacao para o movimento, priorizando capturas de pecas mais valiosas.
    attacker = board.get_piece(*move.start_pos)
    if attacker is None:
        return 0

    if move.is_en_passant:
        end_row, end_col = move.end_pos
        capture_row = end_row + (1 if attacker.color is Color.WHITE else -1)
        victim = board.get_piece(capture_row, end_col)
    else:
        victim = board.get_piece(*move.end_pos)

    if victim is None:
        return 0

    attacker_value = PIECE_VALUES.get(type(attacker), 0)
    victim_value = PIECE_VALUES.get(type(victim), 0)
    return victim_value * 10 - attacker_value


def validate_depth(depth: int) -> None:
    # A busca precisa analisar pelo menos um nivel da arvore.
    if depth < 1:
        raise ValueError("A profundidade deve ser maior ou igual a 1.")


def minimax(
    board,
    depth: int,
    maximizing: bool,
    ai_color: Color,
    alfa: float,
    beta: float,
    deadline: float | None = None,
) -> int:
    if deadline is not None and time.perf_counter() >= deadline:
        raise SearchTimeout

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
                ai_color,
                alfa,
                beta,
                deadline,
            )
            best_value = max(best_value, value)
            alfa = max(alfa, best_value)

            if alfa >= beta:
                break

        return best_value

    best_value = float("inf")

    for _, new_board in successors:
        value = minimax(
            new_board,
            depth - 1,
            True,
            ai_color,
            alfa,
            beta,
            deadline,
        )
        best_value = min(best_value, value)
        beta = min(beta, best_value)
        if alfa >= beta:
            break

    return best_value


def _choose_move_at_depth(
    board,
    ai_color: Color,
    depth: int,
    deadline: float,
):
    successors = expand_node(board, ai_color)
    if not successors:
        return None

    best_move = successors[0][0]
    best_value = float("-inf")
    alfa = float("-inf")
    beta = float("inf")

    for move, new_board in successors:
        if time.perf_counter() >= deadline:
            raise SearchTimeout

        value = minimax(
            new_board,
            depth - 1,
            False,
            ai_color,
            alfa,
            beta,
            deadline,
        )

        if value > best_value:
            best_value = value
            best_move = move
        alfa = max(alfa, best_value)

    return best_move


def choose_minimax_move(
    board,
    ai_color: Color,
    depth: int,
    time_limit_seconds: float = SEARCH_TIME_LIMIT_SECONDS,
):
    # Confere se a profundidade informada pode ser usada na busca.
    validate_depth(depth)

    successors = expand_node(board, ai_color)
    if not successors:
        return None

    best_move = successors[0][0]
    deadline = time.perf_counter() + time_limit_seconds

    for current_depth in range(1, depth + 1):
        try:
            completed_move = _choose_move_at_depth(
                board,
                ai_color,
                current_depth,
                deadline,
            )
            if completed_move is not None:
                best_move = completed_move
        except SearchTimeout:
            break

    return best_move