import unittest

from src.ai.minimax import minimax
from src.domain.board import Board
from src.domain.color import Color


class MinimaxTests(unittest.TestCase):

    def test_minimax_stops_at_depth_zero(self):
        # Confere se a recursao para quando a profundidade chega a zero.
        board = Board()

        value = minimax(
            board,
            depth=0,
            maximizing=True,
            ai_color=Color.WHITE
        )

        self.assertEqual(value, 0)

    def test_minimax_runs_recursively(self):
        # Confere se o minimax consegue percorrer mais de um nivel sem erro.
        board = Board()

        value = minimax(
            board,
            depth=2,
            maximizing=True,
            ai_color=Color.WHITE
        )

        self.assertEqual(value, 0)


if __name__ == "__main__":
    unittest.main()