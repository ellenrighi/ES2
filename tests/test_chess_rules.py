import unittest

from src.application.game import Game
from src.domain.board import Board
from src.domain.color import Color
from src.domain.move import Move
from src.domain.piece import King, Pawn, Rook


class ChessRulesTests(unittest.TestCase):
    """ Testes unitarios para verificar regras de xadrez e fluxo de jogo."""
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
        # Valida o movimento base do peao, incluindo avanco e captura.
        self.skipTest("Pendente: cobertura detalhada das regras basicas do peao.")

    def test_rook_basic_movement_rules(self):
        # Garante que a torre mova em linha reta e respeite bloqueios.
        self.skipTest("Pendente: cobertura detalhada das regras basicas da torre.")

    def test_bishop_basic_movement_rules(self):
        # Garante que o bispo mova apenas em diagonal.
        self.skipTest("Pendente: cobertura detalhada das regras basicas do bispo.")

    def test_knight_basic_movement_rules(self):
        # Garante que o cavalo mova em L e possa saltar pecas.
        self.skipTest("Pendente: cobertura detalhada das regras basicas do cavalo.")

    def test_queen_basic_movement_rules(self):
        # Garante que a dama combine os movimentos da torre e do bispo.
        self.skipTest("Pendente: cobertura detalhada das regras basicas da dama.")

    def test_king_basic_movement_rules(self):
        # Garante que o rei mova uma casa em qualquer direcao.
        self.skipTest("Pendente: cobertura detalhada das regras basicas do rei.")

    def test_move_blocked_by_friendly_piece(self):
        # Confere que uma peca amiga bloqueia o lance e nao pode ser capturada.
        self.skipTest("Pendente: bloqueio por peca amiga e captura valida.")

    def test_castling_queenside_and_restrictions(self):
        # Cobre o roque maior e suas restricoes de passagem e movimento previo.
        self.skipTest("Pendente: roque maior e validacoes de legalidade.")

    def test_en_passant_expires_after_immediate_reply(self):
        # Verifica que o direito de en passant desaparece no lance seguinte.
        self.skipTest("Pendente: expiracao do en passant no turno correto.")

    def test_promotion_supports_all_piece_choices(self):
        # Confere as opcoes de promocao permitidas para o peao.
        self.skipTest("Pendente: promocao para Q, R, B e N.")

    def test_check_detection(self):
        # 1. Posição inicial: nenhum rei deve estar em xeque
        board = Board()
        self.assertFalse(board.is_in_check(Color.WHITE))
        self.assertFalse(board.is_in_check(Color.BLACK))

        # 2. Configuração customizada: Rei em xeque direto
        board.grid = [[None for _ in range(8)] for _ in range(8)]
        board.set_piece(7, 4, King(Color.WHITE))
        board.set_piece(0, 4, Rook(Color.BLACK))

        self.assertTrue(board.is_in_check(Color.WHITE))
        self.assertFalse(board.is_in_check(Color.BLACK))

        # 3. Ataque bloqueado: Peça no meio do caminho impede o xeque
        board.set_piece(6, 4, Pawn(Color.WHITE))
        self.assertFalse(board.is_in_check(Color.WHITE))

    def test_checkmate_detection(self):
        # Prepara a base para validar xeque-mate e fim de jogo.
        self.skipTest("Pendente: deteccao de xeque-mate.")

    def test_stalemate_detection(self):
        # Prepara a base para validar afogamento sem xeque.
        self.skipTest("Pendente: deteccao de afogamento.")

    def test_insufficient_material_detection(self):
        # Valida o empate por material insuficiente.
        self.skipTest("Pendente: empate por material insuficiente.")

    def test_fifty_move_rule_detection(self):
        # Valida o empate pela regra dos 50 lances.
        self.skipTest("Pendente: regra dos 50 lances.")

    def test_threefold_repetition_detection(self):
        # Valida o empate por repeticao tripla da posicao.
        self.skipTest("Pendente: repeticao tripla de posicao.")

    def test_selection_rejects_opponent_piece_out_of_turn(self):
        # Garante que o jogador nao selecione peca da cor adversaria.
        self.skipTest("Pendente: rejeicao de selecao fora do turno.")

    def test_ui_legal_squares_feedback(self):
        # Confere o destaque visual das casas legais apos a selecao.
        self.skipTest("Pendente: feedback visual de casas legais.")


if __name__ == "__main__":
    unittest.main()
