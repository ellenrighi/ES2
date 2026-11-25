from src.ai.difficulty import Difficulty, get_depth
from src.ai.random_ai import choose_random_move
from src.ai.minimax import choose_minimax_move


def choose_ai_move(board, color, difficulty: Difficulty):
    # Escolhe a estrategia da IA de acordo com o nivel de dificuldade.

    if difficulty is Difficulty.EASY:
        return choose_random_move(board, color)

    if difficulty is Difficulty.MEDIUM:
        return choose_minimax_move(
            board,
            color,
            depth=get_depth(Difficulty.MEDIUM)
        )

    if difficulty is Difficulty.HARD:
        return choose_minimax_move(
            board,
            color,
            depth=get_depth(Difficulty.HARD)
        )

    raise ValueError("Dificuldade invalida.")