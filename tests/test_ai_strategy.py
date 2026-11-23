import unittest
from unittest.mock import MagicMock, patch

from src.ai.difficulty import Difficulty
from src.ai.strategy import choose_ai_move
from src.domain.color import Color
from src.domain.move import Move


class AIStrategyTests(unittest.TestCase):

    @patch("src.ai.strategy.choose_random_move")
    def test_easy_uses_random_ai(self, mock_random):
        # O nivel facil deve usar a IA aleatoria.
        board = MagicMock()
        expected_move = Move((6, 0), (5, 0))

        mock_random.return_value = expected_move

        move = choose_ai_move(
            board,
            Color.WHITE,
            Difficulty.EASY
        )

        mock_random.assert_called_once_with(
            board,
            Color.WHITE
        )

        self.assertEqual(move, expected_move)

    @patch("src.ai.strategy.choose_minimax_move")
    def test_medium_uses_minimax_depth_two(self, mock_minimax):
        # O nivel medio deve usar Minimax com profundidade 2.
        board = MagicMock()
        expected_move = Move((6, 0), (5, 0))

        mock_minimax.return_value = expected_move

        move = choose_ai_move(
            board,
            Color.WHITE,
            Difficulty.MEDIUM
        )

        mock_minimax.assert_called_once_with(
            board,
            Color.WHITE,
            depth=2
        )

        self.assertEqual(move, expected_move)

    @patch("src.ai.strategy.choose_minimax_move")
    def test_hard_uses_minimax_depth_four(self, mock_minimax):
        # O nivel dificil deve usar Minimax com profundidade 4.
        board = MagicMock()
        expected_move = Move((6, 0), (5, 0))

        mock_minimax.return_value = expected_move

        move = choose_ai_move(
            board,
            Color.WHITE,
            Difficulty.HARD
        )

        mock_minimax.assert_called_once_with(
            board,
            Color.WHITE,
            depth=4
        )

        self.assertEqual(move, expected_move)

    def test_invalid_difficulty_raises_error(self):
        # Um nivel invalido nao deve ser aceito.
        board = MagicMock()

        with self.assertRaises(ValueError):
            choose_ai_move(
                board,
                Color.WHITE,
                "invalid"
            )


if __name__ == "__main__":
    unittest.main()