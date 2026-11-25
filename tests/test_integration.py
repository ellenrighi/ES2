import unittest
from src.domain.board import Board
from src.application.game import Game
from src.domain.color import Color
from src.ai.difficulty import Difficulty
from src.domain.piece import Pawn, Queen
from src.domain.move import Move

class TestIntegracaoBoardPromocao(unittest.TestCase):
    def test_promocao_peao_no_tabuleiro(self):
        board = Board()
        board.grid = [[None for _ in range(8)] for _ in range(8)]
        board.set_piece(1, 4, Pawn(Color.WHITE))
        movimento = Move((1, 4), (0, 4), requires_promotion=True, promotion_piece="Q")
        board.execute_move(movimento)
        peca = board.get_piece(0, 4)
        self.assertIsInstance(peca, Queen)

class TestIntegracaoBoardPiece(unittest.TestCase):
    def test_peao_integrado_ao_tabuleiro(self):
        board = Board()
        movimentos = board.generate_moves_for_piece(6, 4)
        destinos = [move.end_pos for move in movimentos]
        self.assertIn((5, 4), destinos)
        self.assertIn((4, 4), destinos)

class TestIntegracaoGameIABoard(unittest.TestCase):
    def test_ia_executa_jogada_e_altera_tabuleiro(self):
        game = Game(difficulty=Difficulty.EASY)
        game.current_turn = Color.BLACK
        estado_antes = game.board.position_key()
        movimento = game.play_ai_turn()
        estado_depois = game.board.position_key()
        self.assertIsNotNone(movimento)
        self.assertNotEqual(estado_antes, estado_depois)
        self.assertEqual(game.current_turn, Color.WHITE)

if __name__ == "__main__":
    unittest.main()