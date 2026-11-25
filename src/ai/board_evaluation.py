# Este arquivo calcula uma pontuacao para o estado atual do tabuleiro.
# Essa pontuacao e usada pelo Minimax para decidir quais posicoes sao
# melhores ou piores para a IA.
#
# A avaliacao considera:
# - material: valor das pecas de cada jogador;
# - posicao: ocupacao de casas importantes do tabuleiro;
# - mobilidade: quantidade de movimentos legais disponiveis;
# - estados finais: xeque-mate e empate.

from src.domain.color import Color
from src.ai.material_evaluation import evaluate_material
from src.ai.positional_evaluation import evaluate_position
from src.ai.mobility_evaluation import evaluate_mobility


CHECKMATE_SCORE = 100000


def evaluate_board(board, ai_color: Color) -> int:
    # Verifica primeiro se o jogo terminou em xeque-mate.
    if board.is_checkmate(ai_color):
        return -CHECKMATE_SCORE

    opponent_color = ai_color.opposite()

    if board.is_checkmate(opponent_color):
        return CHECKMATE_SCORE

    # Empate nao favorece nenhum dos jogadores.
    if board.is_stalemate(ai_color) or board.is_stalemate(opponent_color):
        return 0

    # Junta as avaliacoes que ja existem no projeto.
    material_score = evaluate_material(board, ai_color)
    positional_score = evaluate_position(board, ai_color)
    mobility_score = evaluate_mobility(board, ai_color)

    return (
        material_score * 100
        + positional_score * 10
        + mobility_score
    )