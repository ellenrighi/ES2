import unittest
from unittest.mock import MagicMock, call, patch

from src.ai.minimax import (
    minimax,
    expand_node,
    choose_minimax_move,
    validate_depth,
)
from src.ai.board_evaluation import evaluate_board, CHECKMATE_SCORE
from src.domain.board import Board
from src.domain.color import Color
from src.domain.move import Move
from src.domain.piece import Pawn, Queen, Rook


class MinimaxTests(unittest.TestCase):

    def test_minimax_stops_at_depth_zero(self):
        # Confere se na profundidade zero o tabuleiro e avaliado.
        board = Board()

        value = minimax(
            board,
            depth=0,
            maximizing=True,
            ai_color=Color.WHITE,
            alfa=float("-inf"),
            beta=float("inf")
        )

        self.assertEqual(value, evaluate_board(board, Color.WHITE))

    def test_minimax_runs_recursively(self):
        # Confere se o minimax consegue percorrer mais de um nivel sem erro.
        board = Board()

        value = minimax(
            board,
            depth=2,
            maximizing=True,
            ai_color=Color.WHITE,
            alfa=float("-inf"),
            beta=float("inf")
        )

        self.assertIsInstance(value, (int, float))

    def test_expand_node_generates_successors(self):
        # Confere se a expansao gera os proximos estados possiveis.
        board = Board()

        successors = expand_node(board, Color.WHITE)

        self.assertGreater(len(successors), 0)

    def test_expand_node_orders_captures_by_mvv_lva(self):
        board = MagicMock()
        pieces = {
            (4, 0): Pawn(Color.WHITE),
            (3, 1): Queen(Color.BLACK),
            (4, 2): Rook(Color.WHITE),
            (3, 3): Queen(Color.BLACK),
            (4, 4): Pawn(Color.WHITE),
            (3, 5): Pawn(Color.BLACK),
            (3, 6): Pawn(Color.WHITE),
            (3, 7): Pawn(Color.BLACK),
            (6, 0): Pawn(Color.WHITE),
        }
        board.get_piece.side_effect = lambda row, col: pieces.get((row, col))

        en_passant = Move((3, 6), (2, 7), is_en_passant=True)
        pawn_takes_queen = Move((4, 0), (3, 1))
        pawn_takes_pawn = Move((4, 4), (3, 5))
        rook_takes_queen = Move((4, 2), (3, 3))
        quiet_move = Move((6, 0), (5, 0))
        successors = [
            (quiet_move, MagicMock()),
            (en_passant, MagicMock()),
            (pawn_takes_queen, MagicMock()),
            (pawn_takes_pawn, MagicMock()),
            (rook_takes_queen, MagicMock()),
        ]
        board.generate_successors.return_value = successors

        ordered = expand_node(board, Color.WHITE)

        self.assertEqual(
            [move for move, _ in ordered],
            [
                pawn_takes_queen,
                rook_takes_queen,
                en_passant,
                pawn_takes_pawn,
                quiet_move,
            ],
        )

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

    @patch("src.ai.minimax.evaluate_board")
    def test_maximizing_propagates_highest_value(self, mock_evaluate):
        # O nivel MAX deve escolher o maior valor entre os sucessores.
        board = MagicMock()

        board_1 = MagicMock()
        board_2 = MagicMock()
        board_3 = MagicMock()

        board.generate_successors.return_value = [
            (Move((0, 0), (0, 1)), board_1),
            (Move((0, 0), (0, 2)), board_2),
            (Move((0, 0), (0, 3)), board_3),
        ]

        mock_evaluate.side_effect = [10, 30, 20]

        value = minimax(
            board,
            depth=1,
            maximizing=True,
            ai_color=Color.WHITE,
            alfa=float("-inf"),
            beta=float("inf")
        )

        self.assertEqual(value, 30)

    @patch("src.ai.minimax.evaluate_board")
    def test_minimizing_propagates_lowest_value(self, mock_evaluate):
        # O nivel MIN deve escolher o menor valor entre os sucessores.
        board = MagicMock()

        board_1 = MagicMock()
        board_2 = MagicMock()
        board_3 = MagicMock()

        board.generate_successors.return_value = [
            (Move((0, 0), (0, 1)), board_1),
            (Move((0, 0), (0, 2)), board_2),
            (Move((0, 0), (0, 3)), board_3),
        ]

        mock_evaluate.side_effect = [10, 30, 20]

        value = minimax(
            board,
            depth=1,
            maximizing=False,
            ai_color=Color.WHITE,
            alfa=float("-inf"),
            beta=float("inf")
        )

        self.assertEqual(value, 10)

    @patch("src.ai.minimax.minimax")
    def test_choose_minimax_move_selects_best_move(self, mock_minimax):
        # Confere se a IA escolhe a jogada com maior valor.
        board = MagicMock()

        move_1 = Move((6, 0), (5, 0))
        move_2 = Move((6, 1), (4, 1))
        move_3 = Move((6, 2), (5, 2))

        board.generate_successors.return_value = [
            (move_1, MagicMock()),
            (move_2, MagicMock()),
            (move_3, MagicMock()),
        ]

        mock_minimax.side_effect = [10, 50, 20]

        best_move = choose_minimax_move(
            board,
            Color.WHITE,
            depth=2
        )

        self.assertEqual(best_move, move_2)

    @patch("src.ai.minimax.evaluate_board")
    def test_maximizing_prunes_when_alpha_reaches_beta(self, mock_evaluate):
        board = MagicMock()
        board.generate_successors.return_value = [
            (Move((0, 0), (0, 1)), MagicMock()),
            (Move((0, 0), (0, 2)), MagicMock()),
        ]
        mock_evaluate.return_value = 25

        value = minimax(
            board,
            depth=1,
            maximizing=True,
            ai_color=Color.WHITE,
            alfa=10,
            beta=20
        )

        self.assertEqual(value, 25)
        mock_evaluate.assert_called_once()

    @patch("src.ai.minimax.evaluate_board")
    def test_minimizing_prunes_when_beta_reaches_alpha(self, mock_evaluate):
        board = MagicMock()
        board.generate_successors.return_value = [
            (Move((0, 0), (0, 1)), MagicMock()),
            (Move((0, 0), (0, 2)), MagicMock()),
        ]
        mock_evaluate.return_value = 5

        value = minimax(
            board,
            depth=1,
            maximizing=False,
            ai_color=Color.WHITE,
            alfa=10,
            beta=20
        )

        self.assertEqual(value, 5)
        mock_evaluate.assert_called_once()

    def test_choose_minimax_move_returns_none_without_moves(self):
        # Se nao houver jogadas legais, nenhuma jogada deve ser retornada.
        board = MagicMock()
        board.generate_successors.return_value = []

        best_move = choose_minimax_move(
            board,
            Color.WHITE,
            depth=2
        )

        self.assertIsNone(best_move)

    def test_validate_depth_accepts_positive_depth(self):
        # Profundidades a partir de 1 podem ser usadas na busca.
        validate_depth(1)
        validate_depth(3)

    def test_validate_depth_rejects_zero(self):
        # A busca nao deve comecar com profundidade zero.
        with self.assertRaises(ValueError):
            validate_depth(0)

    @patch("src.ai.minimax.minimax")
    def test_choose_move_reduces_depth_before_recursion(self, mock_minimax):
        # Depois da primeira jogada, o nivel seguinte recebe profundidade menor.
        board = MagicMock()
        move = Move((6, 0), (5, 0))
        new_board = MagicMock()

        board.generate_successors.return_value = [
            (move, new_board)
        ]

        mock_minimax.return_value = 10

        choose_minimax_move(
            board,
            Color.WHITE,
            depth=3
        )

        mock_minimax.assert_called_once_with(
            new_board,
            2,
            False,
            Color.WHITE,
            float("-inf"),
            float("inf")
        )

    @patch("src.ai.minimax.minimax")
    def test_choose_move_carries_alpha_to_next_root_branch(self, mock_minimax):
        board = MagicMock()
        move_1 = Move((6, 0), (5, 0))
        move_2 = Move((6, 1), (5, 1))
        board_1 = MagicMock()
        board_2 = MagicMock()
        board.generate_successors.return_value = [
            (move_1, board_1),
            (move_2, board_2),
        ]
        mock_minimax.side_effect = [10, 20]

        choose_minimax_move(board, Color.WHITE, depth=2)

        self.assertEqual(
            mock_minimax.call_args_list,
            [
                call(board_1, 1, False, Color.WHITE, float("-inf"), float("inf")),
                call(board_2, 1, False, Color.WHITE, 10, float("inf")),
            ]
        )


if __name__ == "__main__":
    unittest.main()