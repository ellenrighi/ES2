import unittest

from src.ai.material_evaluation import evaluate_material
from src.domain.board import Board
from src.domain.color import Color
from src.domain.piece import Pawn, Queen


class MaterialEvaluationTests(unittest.TestCase):

    def test_initial_position_has_equal_material(self):
        # No inicio da partida, os dois lados tem o mesmo material.
        board = Board()

        self.assertEqual(evaluate_material(board, Color.WHITE), 0)
        self.assertEqual(evaluate_material(board, Color.BLACK), 0)

    def test_material_advantage_is_positive(self):
        # Se uma cor tem mais material, a avaliacao deve ser positiva para ela.
        board = Board()
        board.grid = [[None for _ in range(8)] for _ in range(8)]

        board.set_piece(4, 4, Queen(Color.WHITE))
        board.set_piece(2, 2, Pawn(Color.BLACK))

        self.assertEqual(evaluate_material(board, Color.WHITE), 8)

    def test_material_advantage_changes_by_color(self):
        # A mesma posicao deve ter valor oposto dependendo da cor avaliada.
        board = Board()
        board.grid = [[None for _ in range(8)] for _ in range(8)]

        board.set_piece(4, 4, Queen(Color.WHITE))
        board.set_piece(2, 2, Pawn(Color.BLACK))

        self.assertEqual(evaluate_material(board, Color.WHITE), 8)
        self.assertEqual(evaluate_material(board, Color.BLACK), -8)


if __name__ == "__main__":
    unittest.main()