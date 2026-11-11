import unittest

from src.ai.positional_evaluation import evaluate_position
from src.domain.board import Board
from src.domain.color import Color
from src.domain.piece import Pawn


class PositionalEvaluationTests(unittest.TestCase):

    def test_initial_position_has_neutral_position_score(self):
        # No inicio nenhuma peca ocupa diretamente o centro.
        board = Board()

        self.assertEqual(evaluate_position(board, Color.WHITE), 0)
        self.assertEqual(evaluate_position(board, Color.BLACK), 0)

    def test_piece_in_center_increases_score(self):
        # Uma peca da cor avaliada no centro deve aumentar a pontuacao.
        board = Board()
        board.grid = [[None for _ in range(8)] for _ in range(8)]

        board.set_piece(3, 3, Pawn(Color.WHITE))

        self.assertEqual(evaluate_position(board, Color.WHITE), 1)

    def test_enemy_piece_in_center_decreases_score(self):
        # Uma peca adversaria no centro deve diminuir a pontuacao.
        board = Board()
        board.grid = [[None for _ in range(8)] for _ in range(8)]

        board.set_piece(3, 3, Pawn(Color.BLACK))

        self.assertEqual(evaluate_position(board, Color.WHITE), -1)


if __name__ == "__main__":
    unittest.main()