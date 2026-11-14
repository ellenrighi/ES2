import unittest
from unittest.mock import MagicMock

from src.ai.minimax import minimax, expand_node
from src.ai.board_evaluation import evaluate_board, CHECKMATE_SCORE
from src.domain.board import Board
from src.domain.color import Color


class MinimaxTests(unittest.TestCase):

    def test_minimax_stops_at_depth_zero(self):
        # Confere se na profundidade zero o tabuleiro e avaliado.
        board = Board()

        value = minimax(
            board,
            depth=0,
            maximizing=True,
            ai_color=Color.WHITE
        )

        self.assertEqual(value, evaluate_board(board, Color.WHITE))

    def test_minimax_runs_recursively(self):
        # Confere se o minimax consegue percorrer mais de um nivel sem erro.
        board = Board()

        value = minimax(
            board,
            depth=2,
            maximizing=True,
            ai_color=Color.WHITE
        )

        self.assertIsInstance(value, (int, float))

    def test_expand_node_generates_successors(self):
        # Confere se a expansao gera os proximos estados possiveis.
        board = Board()

        successors = expand_node(board, Color.WHITE)

        self.assertGreater(len(successors), 0)

    def test_initial_board_has_neutral_evaluation(self):
        # No inicio os dois lados possuem a mesma situacao.
        board = Board()

        value = evaluate_board(board, Color.WHITE)

        self.assertEqual(value, 0)

    def test_checkmate_against_ai_has_negative_score(self):
        # Xeque-mate sofrido pela IA deve receber uma pontuacao muito negativa.
        board = MagicMock()

        board.is_checkmate.side_effect = lambda color: color is Color.WHITE
        board.is_stalemate.return_value = False

        value = evaluate_board(board, Color.WHITE)

        self.assertEqual(value, -CHECKMATE_SCORE)

    def test_checkmate_against_opponent_has_positive_score(self):
        # Xeque-mate no adversario deve receber uma pontuacao muito positiva.
        board = MagicMock()

        board.is_checkmate.side_effect = lambda color: color is Color.BLACK
        board.is_stalemate.return_value = False

        value = evaluate_board(board, Color.WHITE)

        self.assertEqual(value, CHECKMATE_SCORE)


if __name__ == "__main__":
    unittest.main()