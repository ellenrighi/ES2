from interface.screens.ai_levels import AI_LEVELS

AI_DELAY_MS = 800


def update_ai(game, page, elapsed_ms, delta_ms, animation=None):
    """Executa a jogada da IA após a espera, com a partida visível."""
    if animation is not None and animation.active:
        if page in AI_LEVELS:
            animation.advance(delta_ms)
        return 0
    if game is None or not game.can_play_ai:
        return 0
    if page not in AI_LEVELS:
        return elapsed_ms
    next_elapsed = elapsed_ms + delta_ms
    if not (elapsed_ms < AI_DELAY_MS <= next_elapsed):
        return next_elapsed

    previous_board = game.board.copy() if animation is not None else None
    move = game.play_ai_turn()

    if move is not None:
        if animation is not None:
            animation.start(previous_board, move)
        return 0
    return next_elapsed
