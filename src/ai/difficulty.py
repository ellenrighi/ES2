from enum import Enum


class Difficulty(Enum):
    # Niveis de dificuldade disponiveis para a IA.
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"


DIFFICULTY_DEPTH = {
    Difficulty.MEDIUM: 2,
    Difficulty.HARD: 4,
}

def get_depth(difficulty: Difficulty) -> int | None:
    # Retorna a profundidade usada pelo Minimax em cada dificuldade.
    # O nivel facil usa IA aleatoria, por isso nao possui profundidade.
    if difficulty is Difficulty.EASY:
        return None

    return DIFFICULTY_DEPTH[difficulty]