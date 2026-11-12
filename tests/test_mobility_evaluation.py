import unittest

from src.ai.mobility_evaluation import evaluate_mobility
from src.domain.board import Board
from src.domain.color import Color
from src.domain.piece import King, Rook


class MobilityEvaluationTests(unittest.TestCase):

    def test_initial_position_has_balanced_mobility(self):
        # No inicio, os dois lados devem ter mobilidade equivalente.
        board = Board()

        self.assertEqual(evaluate_mobility(board, Color.WHITE), 0)
        self.assertEqual(evaluate_mobility(board, Color.BLACK), 0)

    def test_more_available_moves_gives_positive_score(self):
        # Uma cor com mais movimentos legais deve receber pontuacao positiva.
        board = Board()
        board.grid = [[None for _ in range(8)] for _ in range(8)]

        board.set_piece(7, 7, King(Color.WHITE))
        board.set_piece(4, 4, Rook(Color.WHITE))
        board.set_piece(0, 0, King(Color.BLACK))

        self.assertGreater(
            evaluate_mobility(board, Color.WHITE),
            0
        )

    def test_score_changes_with_evaluated_color(self):
        # A mesma posicao deve favorecer uma cor e desfavorecer a outra.
        board = Board()
        board.grid = [[None for _ in range(8)] for _ in range(8)]

        board.set_piece(7, 7, King(Color.WHITE))
        board.set_piece(4, 4, Rook(Color.WHITE))
        board.set_piece(0, 0, King(Color.BLACK))

        white_score = evaluate_mobility(board, Color.WHITE)
        black_score = evaluate_mobility(board, Color.BLACK)

        self.assertEqual(white_score, -black_score)


if __name__ == "__main__":
    unittest.main()