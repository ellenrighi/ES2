import unittest

from src.application.game import Game
from src.domain.board import Board
from src.domain.color import Color
from src.domain.move import Move
from src.domain.piece import Bishop, King, Knight, Pawn, Queen, Rook


class ChessRulesTests(unittest.TestCase):

    def test_initial_setup_has_kings_and_pawns(self):
        board = Board()
        self.assertIsInstance(board.get_piece(7, 4), King)
        self.assertIsInstance(board.get_piece(0, 4), King)
        self.assertIsInstance(board.get_piece(6, 0), Pawn)
        self.assertIsInstance(board.get_piece(1, 7), Pawn)

    def test_turn_alternates_after_valid_move(self):
        game = Game()
        game.handle_click(6, 4)
        game.handle_click(4, 4)
        self.assertEqual(game.current_turn, Color.BLACK)

    def test_en_passant_generation_and_execution(self):
        board = Board()
        board.grid = [[None for _ in range(8)] for _ in range(8)]
        board.set_piece(3, 4, Pawn(Color.WHITE))
        board.set_piece(1, 5, Pawn(Color.BLACK))

        board.execute_move(Move(start_pos=(1, 5), end_pos=(3, 5)))
        white_moves = board.generate_moves_for_piece(3, 4)
        en_passant = [m for m in white_moves if m.is_en_passant]
        self.assertEqual(len(en_passant), 1)

        board.execute_move(en_passant[0])
        self.assertIsNone(board.get_piece(3, 5))
        self.assertIsNotNone(board.get_piece(2, 5))

    def test_undo_move_restores_previous_position(self):
        board = Board()

        board.execute_move(Move(start_pos=(6, 4), end_pos=(4, 4)))
        board.undo_move()

        self.assertIsInstance(board.get_piece(6, 4), Pawn)
        self.assertIsNone(board.get_piece(4, 4))

    def test_undo_move_restores_captured_piece(self):
        board = Board()
        board.grid = [[None for _ in range(8)] for _ in range(8)]

        board.set_piece(4, 4, Rook(Color.WHITE))
        board.set_piece(4, 6, Pawn(Color.BLACK))

        board.execute_move(Move(start_pos=(4, 4), end_pos=(4, 6)))
        board.undo_move()

        self.assertIsInstance(board.get_piece(4, 4), Rook)
        self.assertIsInstance(board.get_piece(4, 6), Pawn)

    def test_undo_move_restores_piece_state(self):
        board = Board()

        board.execute_move(Move(start_pos=(6, 4), end_pos=(4, 4)))
        moved_pawn = board.get_piece(4, 4)
        self.assertTrue(moved_pawn.has_moved)

        board.undo_move()
        restored_pawn = board.get_piece(6, 4)

        self.assertIsInstance(restored_pawn, Pawn)
        self.assertFalse(restored_pawn.has_moved)

    def test_generate_successors_returns_legal_moves(self):
        board = Board()

        successors = board.generate_successors(Color.WHITE)

        self.assertGreater(len(successors), 0)

        for move, new_board in successors:
            self.assertIsInstance(move, Move)
            self.assertIsInstance(new_board, Board)

    def test_generate_successors_does_not_change_original_board(self):
        board = Board()

        board.generate_successors(Color.WHITE)

        self.assertIsInstance(board.get_piece(6, 4), Pawn)
        self.assertIsNone(board.get_piece(4, 4))

    def test_generate_successors_applies_move_on_copy(self):
        board = Board()

        successors = board.generate_successors(Color.WHITE)

        move, new_board = successors[0]

        self.assertIsNone(new_board.get_piece(*move.start_pos))
        self.assertIsNotNone(new_board.get_piece(*move.end_pos))

    def test_generate_successors_promotes_pawn_to_queen_by_default(self):
        board = Board()
        board.grid = [[None] * 8 for _ in range(8)]
        board.set_piece(7, 7, King(Color.WHITE))
        board.set_piece(0, 0, King(Color.BLACK))
        board.set_piece(1, 4, Pawn(Color.WHITE))

        successors = board.generate_successors(Color.WHITE)
        promotions = [
            (move, new_board)
            for move, new_board in successors
            if move.requires_promotion
        ]

        self.assertEqual(len(promotions), 1)
        move, new_board = promotions[0]
        self.assertEqual(move.promotion_piece, "Q")
        promoted_piece = new_board.get_piece(*move.end_pos)
        self.assertIsInstance(promoted_piece, Queen)

    def test_castling_kingside_available_when_path_clear(self):
        board = Board()
        board.set_piece(7, 5, None)
        board.set_piece(7, 6, None)
        king_moves = board.generate_moves_for_piece(7, 4)
        self.assertTrue(any(m.is_castling and m.end_pos == (7, 6) for m in king_moves))

    def test_promotion_requires_choice_and_applies_piece(self):
        game = Game()
        board = game.board
        board.grid = [[None for _ in range(8)] for _ in range(8)]
        board.set_piece(1, 0, Pawn(Color.WHITE))
        game.current_turn = Color.WHITE

        game.handle_click(1, 0)
        game.handle_click(0, 0)
        self.assertIsNotNone(game.pending_promotion_move)

        game.choose_promotion("R")
        promoted = board.get_piece(0, 0)
        self.assertIsInstance(promoted, Rook)
        self.assertEqual(game.current_turn, Color.BLACK)

    def test_pinned_piece_cannot_expose_king(self):
        board = Board()
        board.grid = [[None for _ in range(8)] for _ in range(8)]

        board.set_piece(7, 4, King(Color.WHITE))
        board.set_piece(6, 4, Rook(Color.WHITE))
        board.set_piece(0, 4, Rook(Color.BLACK))

        moves = board.generate_moves_for_piece(6, 4)

        self.assertFalse(
            any(move.end_pos == (6, 3) for move in moves)
        )

    def test_king_cannot_move_into_check(self):
        board = Board()
        board.grid = [[None for _ in range(8)] for _ in range(8)]

        board.set_piece(7, 4, King(Color.WHITE))
        board.set_piece(6, 0, Rook(Color.BLACK))

        moves = board.generate_moves_for_piece(7, 4)

        self.assertFalse(
            any(move.end_pos == (6, 4) for move in moves)
        )

    def test_pawn_basic_movement_rules(self):
        board = Board()
        board.grid = [[None for _ in range(8)] for _ in range(8)]
        board.set_piece(7, 0, King(Color.WHITE))
        board.set_piece(0, 7, King(Color.BLACK))

        board.set_piece(6, 3, Pawn(Color.WHITE))
        moves = board.generate_moves_for_piece(6, 3)
        end_positions = {m.end_pos for m in moves}
        self.assertEqual(end_positions, {(5, 3), (4, 3)})

        board.set_piece(5, 3, Pawn(Color.BLACK))
        blocked_moves = board.generate_moves_for_piece(6, 3)
        self.assertEqual(blocked_moves, [])

        board.set_piece(5, 2, Pawn(Color.BLACK))
        capture_moves = board.generate_moves_for_piece(6, 3)
        capture_end_positions = {m.end_pos for m in capture_moves}
        self.assertEqual(capture_end_positions, {(5, 2)})

        board.set_piece(6, 3, None)
        board.set_piece(5, 3, None)
        board.set_piece(5, 2, None)
        board.set_piece(5, 3, Pawn(Color.WHITE, has_moved=True))
        moved_pawn_moves = board.generate_moves_for_piece(5, 3)
        self.assertEqual({m.end_pos for m in moved_pawn_moves}, {(4, 3)})

    def test_rook_basic_movement_rules(self):
        board = Board()
        board.grid = [[None for _ in range(8)] for _ in range(8)]
        board.set_piece(7, 7, King(Color.WHITE))
        board.set_piece(0, 0, King(Color.BLACK))

        board.set_piece(4, 4, Rook(Color.WHITE))
        moves = board.generate_moves_for_piece(4, 4)
        end_positions = {m.end_pos for m in moves}
        self.assertEqual(len(end_positions), 14)
        self.assertIn((4, 0), end_positions)
        self.assertIn((4, 7), end_positions)
        self.assertIn((1, 4), end_positions)
        self.assertIn((7, 4), end_positions)

        board.set_piece(4, 6, Pawn(Color.WHITE))
        board.set_piece(2, 4, Pawn(Color.BLACK))
        new_moves = {m.end_pos for m in board.generate_moves_for_piece(4, 4)}
        self.assertIn((4, 5), new_moves)
        self.assertNotIn((4, 6), new_moves)
        self.assertNotIn((4, 7), new_moves)
        self.assertIn((3, 4), new_moves)
        self.assertIn((2, 4), new_moves)
        self.assertNotIn((1, 4), new_moves)

    def test_bishop_basic_movement_rules(self):
        board = Board()
        board.grid = [[None for _ in range(8)] for _ in range(8)]
        board.set_piece(7, 0, King(Color.WHITE))
        board.set_piece(0, 7, King(Color.BLACK))

        board.set_piece(4, 4, Bishop(Color.WHITE))
        moves = board.generate_moves_for_piece(4, 4)
        end_positions = {m.end_pos for m in moves}
        for r, c in end_positions:
            self.assertEqual(abs(r - 4), abs(c - 4))
        self.assertIn((1, 1), end_positions)
        self.assertIn((7, 1), end_positions)
        self.assertIn((1, 7), end_positions)

        board.set_piece(2, 2, Pawn(Color.WHITE))
        board.set_piece(6, 6, Pawn(Color.BLACK))
        new_moves = {m.end_pos for m in board.generate_moves_for_piece(4, 4)}
        self.assertIn((3, 3), new_moves)
        self.assertNotIn((2, 2), new_moves)
        self.assertNotIn((1, 1), new_moves)
        self.assertIn((5, 5), new_moves)
        self.assertIn((6, 6), new_moves)
        self.assertNotIn((7, 7), new_moves)

    def test_knight_basic_movement_rules(self):
        board = Board()
        board.grid = [[None for _ in range(8)] for _ in range(8)]
        board.set_piece(7, 0, King(Color.WHITE))
        board.set_piece(0, 7, King(Color.BLACK))

        board.set_piece(4, 4, Knight(Color.WHITE))
        moves = board.generate_moves_for_piece(4, 4)
        end_positions = {m.end_pos for m in moves}
        expected = {(2, 3), (2, 5), (3, 2), (3, 6), (5, 2), (5, 6), (6, 3), (6, 5)}
        self.assertEqual(end_positions, expected)

        board.set_piece(3, 4, Pawn(Color.WHITE))
        board.set_piece(4, 3, Pawn(Color.WHITE))
        board.set_piece(5, 4, Pawn(Color.BLACK))
        board.set_piece(4, 5, Pawn(Color.BLACK))
        self.assertEqual({m.end_pos for m in board.generate_moves_for_piece(4, 4)}, expected)

        board.set_piece(2, 3, Pawn(Color.WHITE))
        board.set_piece(2, 5, Pawn(Color.BLACK))
        filtered = {m.end_pos for m in board.generate_moves_for_piece(4, 4)}
        self.assertNotIn((2, 3), filtered)
        self.assertIn((2, 5), filtered)

    def test_queen_basic_movement_rules(self):
        board = Board()
        board.grid = [[None for _ in range(8)] for _ in range(8)]
        board.set_piece(7, 0, King(Color.WHITE))
        board.set_piece(0, 2, King(Color.BLACK))

        board.set_piece(4, 4, Queen(Color.WHITE))
        moves = board.generate_moves_for_piece(4, 4)
        end_positions = {m.end_pos for m in moves}
        self.assertEqual(len(end_positions), 27)

        board.set_piece(4, 6, Pawn(Color.WHITE))
        board.set_piece(2, 2, Pawn(Color.WHITE))
        board.set_piece(4, 2, Pawn(Color.BLACK))
        board.set_piece(6, 6, Pawn(Color.BLACK))
        new_positions = {m.end_pos for m in board.generate_moves_for_piece(4, 4)}
        self.assertIn((4, 5), new_positions)
        self.assertNotIn((4, 6), new_positions)
        self.assertIn((3, 3), new_positions)
        self.assertNotIn((2, 2), new_positions)
        self.assertIn((4, 2), new_positions)
        self.assertNotIn((4, 1), new_positions)
        self.assertIn((6, 6), new_positions)
        self.assertNotIn((7, 7), new_positions)

    def test_king_basic_movement_rules(self):
        board = Board()
        board.grid = [[None for _ in range(8)] for _ in range(8)]
        board.set_piece(0, 0, King(Color.BLACK))
        board.set_piece(4, 4, King(Color.WHITE))

        moves = board.generate_moves_for_piece(4, 4)
        end_positions = {m.end_pos for m in moves}
        expected = {(3, 3), (3, 4), (3, 5), (4, 3), (4, 5), (5, 3), (5, 4), (5, 5)}
        self.assertEqual(end_positions, expected)

        board.set_piece(3, 4, Pawn(Color.WHITE))
        board.set_piece(5, 5, Pawn(Color.BLACK))
        filtered = {m.end_pos for m in board.generate_moves_for_piece(4, 4)}
        self.assertNotIn((3, 4), filtered)
        self.assertIn((5, 5), filtered)

    def test_move_blocked_by_friendly_piece(self):
        board = Board()
        board.grid = [[None for _ in range(8)] for _ in range(8)]
        board.set_piece(7, 4, King(Color.WHITE))
        board.set_piece(0, 4, King(Color.BLACK))

        board.set_piece(7, 0, Rook(Color.WHITE))
        board.set_piece(7, 1, Pawn(Color.WHITE))
        moves = board.generate_moves_for_piece(7, 0)
        self.assertNotIn((7, 1), {m.end_pos for m in moves})

        board.set_piece(7, 1, Pawn(Color.BLACK))
        moves_after = board.generate_moves_for_piece(7, 0)
        self.assertIn((7, 1), {m.end_pos for m in moves_after})

    def test_castling_queenside_and_restrictions(self):
        board = Board()
        board.grid = [[None for _ in range(8)] for _ in range(8)]
        board.set_piece(7, 4, King(Color.WHITE))
        board.set_piece(7, 0, Rook(Color.WHITE))
        board.set_piece(0, 4, King(Color.BLACK))

        king_moves = board.generate_moves_for_piece(7, 4)
        self.assertTrue(any(m.is_castling and m.end_pos == (7, 2) for m in king_moves))

        queenside_move = next(m for m in king_moves if m.is_castling and m.end_pos == (7, 2))
        board.execute_move(queenside_move)
        self.assertIsInstance(board.get_piece(7, 2), King)
        self.assertIsInstance(board.get_piece(7, 3), Rook)
        self.assertIsNone(board.get_piece(7, 4))
        self.assertIsNone(board.get_piece(7, 0))

        board = Board()
        board.grid = [[None for _ in range(8)] for _ in range(8)]
        king = King(Color.WHITE)
        king.has_moved = True
        board.set_piece(7, 4, king)
        board.set_piece(7, 0, Rook(Color.WHITE))
        board.set_piece(0, 4, King(Color.BLACK))
        self.assertFalse(any(m.is_castling for m in board.generate_moves_for_piece(7, 4)))

        board = Board()
        board.grid = [[None for _ in range(8)] for _ in range(8)]
        rook = Rook(Color.WHITE)
        rook.has_moved = True
        board.set_piece(7, 4, King(Color.WHITE))
        board.set_piece(7, 0, rook)
        board.set_piece(0, 4, King(Color.BLACK))
        self.assertFalse(any(m.is_castling for m in board.generate_moves_for_piece(7, 4)))

        board = Board()
        board.grid = [[None for _ in range(8)] for _ in range(8)]
        board.set_piece(7, 4, King(Color.WHITE))
        board.set_piece(7, 0, Rook(Color.WHITE))
        board.set_piece(0, 4, Rook(Color.BLACK))
        self.assertFalse(any(m.is_castling for m in board.generate_moves_for_piece(7, 4)))

        board = Board()
        board.grid = [[None for _ in range(8)] for _ in range(8)]
        board.set_piece(7, 4, King(Color.WHITE))
        board.set_piece(7, 0, Rook(Color.WHITE))
        board.set_piece(0, 3, Rook(Color.BLACK))
        self.assertFalse(any(m.is_castling for m in board.generate_moves_for_piece(7, 4)))

        board = Board()
        board.grid = [[None for _ in range(8)] for _ in range(8)]
        board.set_piece(7, 4, King(Color.WHITE))
        board.set_piece(7, 0, Rook(Color.WHITE))
        board.set_piece(7, 1, Knight(Color.WHITE))
        self.assertFalse(any(m.is_castling for m in board.generate_moves_for_piece(7, 4)))

    def test_en_passant_expires_after_immediate_reply(self):
        board = Board()
        board.grid = [[None for _ in range(8)] for _ in range(8)]
        board.set_piece(7, 7, King(Color.WHITE))
        board.set_piece(0, 0, King(Color.BLACK))

        board.set_piece(6, 4, Pawn(Color.WHITE))
        board.set_piece(4, 3, Pawn(Color.BLACK))
        board.set_piece(0, 1, Knight(Color.BLACK))

        board.execute_move(Move(start_pos=(6, 4), end_pos=(4, 4)))
        self.assertEqual(board.en_passant_target, (5, 4))
        black_moves = board.generate_moves_for_piece(4, 3)
        self.assertTrue(any(m.is_en_passant for m in black_moves))

        board.execute_move(Move(start_pos=(0, 1), end_pos=(2, 2)))
        self.assertIsNone(board.en_passant_target)

        board.execute_move(Move(start_pos=(7, 7), end_pos=(7, 6)))

        black_moves_after = board.generate_moves_for_piece(4, 3)
        self.assertFalse(any(m.is_en_passant for m in black_moves_after))

    def test_promotion_supports_all_piece_choices(self):
        choices = [
            ("Q", Queen),
            ("R", Rook),
            ("B", Bishop),
            ("N", Knight),
        ]
        for code, expected_cls in choices:
            game = Game()
            game.board.grid = [[None for _ in range(8)] for _ in range(8)]
            game.board.set_piece(1, 0, Pawn(Color.WHITE))
            game.board.set_piece(7, 7, King(Color.WHITE))
            game.board.set_piece(0, 7, King(Color.BLACK))
            game.current_turn = Color.WHITE

            game.handle_click(1, 0)
            game.handle_click(0, 0)
            self.assertIsNotNone(game.pending_promotion_move)

            game.choose_promotion(code)
            promoted_piece = game.board.get_piece(0, 0)
            self.assertIsInstance(promoted_piece, expected_cls)
            self.assertEqual(promoted_piece.color, Color.WHITE)
            self.assertEqual(game.current_turn, Color.BLACK)

    def test_check_detection(self):
        board = Board()
        self.assertFalse(board.is_in_check(Color.WHITE))
        self.assertFalse(board.is_in_check(Color.BLACK))

        board.grid = [[None for _ in range(8)] for _ in range(8)]
        board.set_piece(7, 4, King(Color.WHITE))
        board.set_piece(0, 4, Rook(Color.BLACK))

        self.assertTrue(board.is_in_check(Color.WHITE))
        self.assertFalse(board.is_in_check(Color.BLACK))

        board.set_piece(6, 4, Pawn(Color.WHITE))
        self.assertFalse(board.is_in_check(Color.WHITE))

    def test_checkmate_detection(self):
        board = Board()
        board.grid = [[None for _ in range(8)] for _ in range(8)]

        board.set_piece(7, 7, King(Color.WHITE))
        board.set_piece(5, 7, King(Color.BLACK))
        board.set_piece(6, 7, Queen(Color.BLACK))

        self.assertTrue(board.is_checkmate(Color.WHITE))
        self.assertFalse(board.is_checkmate(Color.BLACK))

    def test_game_checkmate_displays_winner_and_stops_moves(self):
        game = Game()
        game.board.grid = [[None for _ in range(8)] for _ in range(8)]
        game.board.set_piece(7, 7, King(Color.WHITE))
        game.board.set_piece(5, 7, King(Color.BLACK))
        game.board.set_piece(6, 7, Queen(Color.BLACK))
        game.current_turn = Color.WHITE

        game._evaluate_checkmate()

        self.assertTrue(game.game_over)
        self.assertIs(game.winner, Color.BLACK)
        self.assertEqual(game.status_message, "Pecas pretas venceram")
        before = repr(game.board.grid)
        game.handle_click(7, 7)
        self.assertEqual(repr(game.board.grid), before)

    def test_stalemate_detection(self):
        board = Board()
        board.grid = [[None for _ in range(8)] for _ in range(8)]

        board.set_piece(7, 7, King(Color.WHITE))
        board.set_piece(5, 6, King(Color.BLACK))
        board.set_piece(6, 5, Queen(Color.BLACK))

        self.assertFalse(board.is_in_check(Color.WHITE))
        self.assertTrue(board.is_stalemate(Color.WHITE))
        self.assertFalse(board.is_checkmate(Color.WHITE))

    def test_threefold_repetition_detection(self):
        board = Board()
        knight_cycle = [
            Move(start_pos=(7, 6), end_pos=(5, 5)),
            Move(start_pos=(0, 6), end_pos=(2, 5)),
            Move(start_pos=(5, 5), end_pos=(7, 6)),
            Move(start_pos=(2, 5), end_pos=(0, 6)),
        ]

        for _ in range(2):
            for move in knight_cycle:
                board.execute_move(move)

        self.assertTrue(board.is_threefold_repetition())

    def test_game_repetition_displays_draw_and_stops_moves(self):
        game = Game()
        game.board.position_counts = {game.board.position_key(): 3}

        game._evaluate_checkmate()

        self.assertTrue(game.game_over)
        self.assertIsNone(game.winner)
        self.assertEqual(game.status_message, "Empate por repeticao tripla")
        before = repr(game.board.grid)
        game.handle_click(6, 4)
        self.assertEqual(repr(game.board.grid), before)

    def test_insufficient_material_detection(self):
        board = Board()

        board.grid = [[None for _ in range(8)] for _ in range(8)]
        board.set_piece(7, 4, King(Color.WHITE))
        board.set_piece(0, 4, King(Color.BLACK))
        self.assertTrue(board.is_insufficient_material())

        board.set_piece(5, 2, Bishop(Color.WHITE))
        self.assertTrue(board.is_insufficient_material())

        board.set_piece(5, 2, Knight(Color.WHITE))
        self.assertTrue(board.is_insufficient_material())

        board.grid = [[None for _ in range(8)] for _ in range(8)]
        board.set_piece(7, 4, King(Color.WHITE))
        board.set_piece(0, 4, King(Color.BLACK))
        board.set_piece(7, 2, Bishop(Color.WHITE))
        board.set_piece(0, 5, Bishop(Color.BLACK))
        self.assertTrue(board.is_insufficient_material())

        board.set_piece(0, 5, None)
        board.set_piece(0, 4, King(Color.BLACK))
        board.set_piece(0, 2, Bishop(Color.BLACK))
        self.assertFalse(board.is_insufficient_material())

        board.set_piece(6, 0, Pawn(Color.WHITE))
        self.assertFalse(board.is_insufficient_material())

    def test_fifty_move_rule_detection(self):
        board = Board()
        board.grid = [[None for _ in range(8)] for _ in range(8)]
        board.set_piece(7, 4, King(Color.WHITE))
        board.set_piece(0, 4, King(Color.BLACK))
        board.set_piece(7, 6, Knight(Color.WHITE))
        board.set_piece(0, 6, Knight(Color.BLACK))

        board.halfmove_clock = 99
        self.assertFalse(board.is_fifty_move_rule())

        board.execute_move(Move(start_pos=(7, 6), end_pos=(5, 5)))
        self.assertEqual(board.halfmove_clock, 100)
        self.assertTrue(board.is_fifty_move_rule())

        board.undo_move()
        self.assertEqual(board.halfmove_clock, 99)
        self.assertFalse(board.is_fifty_move_rule())

        board.set_piece(6, 0, Pawn(Color.WHITE))
        board.execute_move(Move(start_pos=(6, 0), end_pos=(5, 0)))
        self.assertEqual(board.halfmove_clock, 0)
        self.assertFalse(board.is_fifty_move_rule())

    def test_selection_rejects_opponent_piece_out_of_turn(self):
        game = Game()
        self.assertEqual(game.current_turn, Color.WHITE)

        game.handle_click(1, 0)
        self.assertIsNone(game.selected_square)
        self.assertEqual(game.status_message, "Selecione uma peca do turno atual.")

    def test_ui_legal_squares_feedback(self):
        game = Game()
        self.assertEqual(game.selected_square, None)
        self.assertEqual(game.legal_moves_by_dest, {})

        game.handle_click(6, 4)
        self.assertEqual(game.selected_square, (6, 4))
        self.assertIn((5, 4), game.legal_moves_by_dest)
        self.assertIn((4, 4), game.legal_moves_by_dest)
        self.assertEqual(game.status_message, "Pawn selecionada.")

        game.handle_click(4, 4)
        self.assertIsNone(game.selected_square)
        self.assertEqual(game.legal_moves_by_dest, {})

    def test_game_stalemate_displays_draw_and_stops_moves(self):
        game = Game()
        game.board.grid = [[None for _ in range(8)] for _ in range(8)]
        game.board.set_piece(7, 7, King(Color.WHITE))
        game.board.set_piece(5, 6, King(Color.BLACK))
        game.board.set_piece(6, 5, Queen(Color.BLACK))
        game.current_turn = Color.WHITE

        game._evaluate_checkmate()

        self.assertTrue(game.game_over)
        self.assertEqual(game.status_message, "Empate por afogamento")

    def test_game_fifty_move_rule_displays_draw_and_stops_moves(self):
        game = Game()
        game.board.halfmove_clock = 100

        game._evaluate_checkmate()

        self.assertTrue(game.game_over)
        self.assertEqual(game.status_message, "Empate pela regra dos 50 lances")

    def test_game_insufficient_material_displays_draw_and_stops_moves(self):
        game = Game()
        game.board.grid = [[None for _ in range(8)] for _ in range(8)]
        game.board.set_piece(7, 4, King(Color.WHITE))
        game.board.set_piece(0, 4, King(Color.BLACK))

        game._evaluate_checkmate()

        self.assertTrue(game.game_over)
        self.assertEqual(game.status_message, "Empate por material insuficiente")


if __name__ == "__main__":
    unittest.main()
