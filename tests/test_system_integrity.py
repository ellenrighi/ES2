import unittest
import random
import time

from src.ai.difficulty import Difficulty
from src.application.game import Game
from src.domain.color import Color
from src.domain.piece import King, Pawn, Queen


def simulate_game(
    difficulty=Difficulty.EASY,
    seed=7,
    max_plies=60,
):
    rng = random.Random(seed)
    game = Game(difficulty)
    metrics = {
        "difficulty": difficulty.value,
        "seed": seed,
        "max_plies": max_plies,
        "plies": 0,
        "captures": 0,
        "promotions": 0,
        "ai_moves": 0,
        "white_moves": 0,
        "black_moves": 0,
        "elapsed_seconds": 0.0,
        "game_over": False,
        "winner": None,
        "status": None,
        "kings_integral": True,
    }

    started_at = time.perf_counter()

    while not game.game_over and game.move_count < max_plies:
        if game.current_turn is Color.WHITE:
            moves = []
            for row in range(8):
                for col in range(8):
                    piece = game.get_piece(row, col)
                    if piece is not None and piece.color is Color.WHITE:
                        moves.extend(game.board.generate_moves_for_piece(row, col))

            if not moves:
                break

            move = rng.choice(moves)
            victim = game.get_piece(*move.end_pos)
            if victim is not None or move.is_en_passant:
                metrics["captures"] += 1
            if move.requires_promotion:
                metrics["promotions"] += 1

            game.handle_click(*move.start_pos)
            game.handle_click(*move.end_pos)
            if move.requires_promotion:
                game.choose_promotion("Q")
            metrics["white_moves"] += 1
        else:
            before_count = game.move_count
            board_before = [
                [game.get_piece(row, col) for col in range(8)]
                for row in range(8)
            ]

            ai_move = game.play_ai_turn()
            if ai_move is None:
                break

            victim_before = board_before[ai_move.end_pos[0]][ai_move.end_pos[1]]
            if victim_before is not None or ai_move.is_en_passant:
                metrics["captures"] += 1
            if ai_move.requires_promotion:
                metrics["promotions"] += 1
            if game.move_count == before_count + 1:
                metrics["ai_moves"] += 1
                metrics["black_moves"] += 1

        metrics["plies"] = game.move_count

        kings = [
            piece
            for row in range(8)
            for col in range(8)
            for piece in [game.get_piece(row, col)]
            if isinstance(piece, King)
        ]
        metrics["kings_integral"] = len(kings) == 2

    metrics["elapsed_seconds"] = time.perf_counter() - started_at
    metrics["game_over"] = game.game_over
    metrics["winner"] = (
        game.winner.value if game.winner is not None else None
    )
    metrics["status"] = game.status_message
    return metrics


class SystemIntegrityTests(unittest.TestCase):

    def test_public_game_flow_keeps_position_consistent(self):
        game = Game(Difficulty.MEDIUM)

        human_moves = [
            ((6, 4), (4, 4)),
            ((7, 6), (5, 5)),
            ((6, 3), (4, 3)),
        ]

        for round_number, (start, end) in enumerate(human_moves, start=1):
            before_count = game.move_count

            game.handle_click(*start)
            game.handle_click(*end)

            self.assertEqual(game.move_count, before_count + 1)
            self.assertEqual(game.current_turn, Color.BLACK)
            self.assertFalse(game.game_over)
            self.assertIsNone(game.selected_square)
            self.assertEqual(game.legal_moves_by_dest, {})

            ai_move = game.play_ai_turn()

            self.assertIsNotNone(ai_move)
            self.assertEqual(game.move_count, before_count + 2)
            self.assertEqual(game.current_turn, Color.WHITE)
            self.assertIsNone(game.get_piece(*ai_move.start_pos))
            self.assertIsNotNone(game.get_piece(*ai_move.end_pos))
            self.assertEqual(
                game.get_piece(*ai_move.end_pos).color,
                Color.BLACK,
            )
            self.assertEqual(game.last_move, ai_move)

            kings = [
                piece
                for row in range(8)
                for col in range(8)
                for piece in [game.get_piece(row, col)]
                if isinstance(piece, King)
            ]
            self.assertEqual(len(kings), 2)
            self.assertIn(game.status_message, ("Turno: Brancas", "Turno: Pretas"))

            self.assertEqual(game.move_count, round_number * 2)

    def test_promotion_and_reset_remain_integral(self):
        game = Game(Difficulty.MEDIUM)
        game.board.grid = [[None] * 8 for _ in range(8)]
        game.board.set_piece(7, 7, King(Color.WHITE))
        game.board.set_piece(0, 0, King(Color.BLACK))
        game.board.set_piece(1, 4, Pawn(Color.WHITE))

        game.handle_click(1, 4)
        game.handle_click(0, 4)

        self.assertIsNotNone(game.pending_promotion_move)
        self.assertIsNone(game.pending_promotion_move.promotion_piece)

        game.choose_promotion("q")

        self.assertIsInstance(game.get_piece(0, 4), Queen)
        self.assertEqual(game.get_piece(0, 4).color, Color.WHITE)
        self.assertIsNone(game.pending_promotion_move)
        self.assertEqual(game.move_count, 1)
        self.assertEqual(game.current_turn, Color.BLACK)

        game.reset()

        self.assertEqual(game.move_count, 0)
        self.assertIsNone(game.last_move)
        self.assertEqual(game.current_turn, Color.WHITE)
        self.assertFalse(game.game_over)
        self.assertIsNone(game.winner)
        self.assertIsInstance(game.get_piece(7, 4), King)
        self.assertIsInstance(game.get_piece(6, 4), Pawn)
        self.assertIsNone(game.selected_square)
        self.assertEqual(game.legal_moves_by_dest, {})

    def test_invalid_move_does_not_mutate_public_state(self):
        game = Game(Difficulty.EASY)
        before_count = game.move_count
        before_piece = game.get_piece(6, 4)

        game.handle_click(6, 4)
        game.handle_click(3, 4)

        self.assertEqual(game.move_count, before_count)
        self.assertIs(game.get_piece(6, 4), before_piece)
        self.assertIsNotNone(game.get_piece(6, 4))
        self.assertIsNone(game.get_piece(3, 4))
        self.assertEqual(game.current_turn, Color.WHITE)

    def test_full_game_simulation_reports_integrity_metrics(self):
        metrics = simulate_game(
            difficulty=Difficulty.EASY,
            seed=7,
            max_plies=60,
        )

        valid_statuses = (
            "Turno: Brancas",
            "Turno: Pretas",
            "Empate por afogamento",
            "Empate por repeticao tripla",
            "Empate pela regra dos 50 lances",
            "Empate por material insuficiente",
            "Pecas brancas venceram",
            "Pecas pretas venceram",
        )
        checks = {
            "Existe ao menos um lance": metrics["plies"] > 0,
            "Contagem de lances consistente": (
                metrics["plies"]
                == metrics["white_moves"] + metrics["black_moves"]
            ),
            "Movimentos da IA registrados": metrics["ai_moves"] >= 0,
            "Capturas registradas": metrics["captures"] >= 0,
            "Promocoes registradas": metrics["promotions"] >= 0,
            "Dois reis presentes": metrics["kings_integral"],
            "Tempo de simulacao valido": metrics["elapsed_seconds"] >= 0,
            "Status final valido": metrics["status"] in valid_statuses,
        }

        print("\n[SYSTEM TEST] Simulacao ponta a ponta")
        print(
            "[METRICAS]"
            f" dificuldade={metrics['difficulty']}"
            f" seed={metrics['seed']}"
            f" lances={metrics['plies']}"
            f" brancas={metrics['white_moves']}"
            f" pretas={metrics['black_moves']}"
            f" ia={metrics['ai_moves']}"
            f" capturas={metrics['captures']}"
            f" promocoes={metrics['promotions']}"
            f" tempo={metrics['elapsed_seconds']:.3f}s"
            f" status={metrics['status']}"
        )
        for label, passed in checks.items():
            print(f"[CHECK] {'PASS' if passed else 'FAIL'} - {label}")
        
        self.assertTrue(all(checks.values()))


if __name__ == "__main__":
    unittest.main()
