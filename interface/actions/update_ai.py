from src.domain.color import Color

AI_DELAY_MS = 800


def update_ai(game, page, elapsed_ms, delta_ms, animation=None):
    """Conta o tempo da IA sem bloquear a janela; pausa fora da partida."""
    if animation is not None and animation.active:
        if page == 'ai_easy':
            animation.advance(delta_ms)
        return 0
    if game.current_turn is not Color.BLACK or game.pending_promotion_move is not None:
        return 0
    if page != 'ai_easy':
        return elapsed_ms
    next_elapsed = elapsed_ms + delta_ms
    if elapsed_ms < AI_DELAY_MS <= next_elapsed:
        previous_board = game.board.copy() if animation is not None else None
        move = game.play_ai_turn()
        if animation is not None and move is not None:
            animation.start(previous_board, move)
        if game.current_turn is Color.WHITE:
            return 0
    return next_elapsed
