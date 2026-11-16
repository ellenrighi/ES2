import unittest
from unittest.mock import MagicMock, patch

from src.ai.minimax import minimax
from src.domain.color import Color
from src.domain.move import Move
from src.domain.piece import Pawn, Queen


class AIPerformanceTests(unittest.TestCase):

    @patch("src.ai.minimax.evaluate_board")
    def test_mvv_lva_ordering_reduces_leaf_evaluations(self, mock_evaluate):
        board = MagicMock()
        quiet_child = MagicMock(score=5)
        capture_child = MagicMock(score=-10)
        quiet_move = Move((6, 0), (5, 0))
        capture_move = Move((4, 0), (3, 1))

        pieces = {
            (6, 0): Pawn(Color.WHITE),
            (4, 0): Pawn(Color.WHITE),
            (3, 1): Queen(Color.BLACK),
        }
        board.get_piece.side_effect = lambda row, col: pieces.get((row, col))
        board.generate_successors.return_value = [
            (quiet_move, quiet_child),
            (capture_move, capture_child),
        ]
        mock_evaluate.side_effect = lambda child, _: child.score

        ordered_value = minimax(
            board,
            depth=1,
            maximizing=False,
            ai_color=Color.WHITE,
            alfa=0,
            beta=float("inf"),
        )
        ordered_evaluations = mock_evaluate.call_count

        mock_evaluate.reset_mock()
        with patch(
            "src.ai.minimax.expand_node",
            side_effect=lambda current_board, color: (
                current_board.generate_successors(color)
            ),
        ):
            unordered_value = minimax(
                board,
                depth=1,
                maximizing=False,
                ai_color=Color.WHITE,
                alfa=0,
                beta=float("inf"),
            )
        unordered_evaluations = mock_evaluate.call_count

        self.assertEqual(ordered_value, unordered_value)
        self.assertEqual(ordered_evaluations, 1)
        self.assertEqual(unordered_evaluations, 2)


if __name__ == "__main__":
    unittest.main()
