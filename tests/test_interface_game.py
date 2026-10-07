import os
os.environ.setdefault('SDL_VIDEODRIVER', 'dummy')
os.environ.setdefault('SDL_AUDIODRIVER', 'dummy')

import unittest
from types import SimpleNamespace
from unittest.mock import patch

import pygame

from interface.actions.draw import draw
from interface.actions.update_ai import update_ai
from interface.components.move_animation import MoveAnimation
from interface.components.exit_popup import EXIT_BUTTONS
from interface.components.draw_board import draw_board
from src.domain.move import Move
from interface.actions.handle_event import handle_event
from interface.components.draw_board import BOARD, SQUARE_SIZE
from interface.components.promotion_popup import PROMOTION_OPTIONS
from interface.components.rules_popup import RULES_BUTTONS
from interface.screens.multiplayer import AI_BUTTONS, MULTIPLAYER_BUTTONS
from interface.screens.ai_levels import AI_LEVEL_BUTTONS
from interface.screens.modes import MODE_BUTTONS
from src.application.game import Game
from src.domain.color import Color
from src.domain.piece import Pawn, Rook


class InterfaceGameTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pygame.init()
        pygame.display.set_mode((800, 600))

    @classmethod
    def tearDownClass(cls):
        pygame.quit()

    def setUp(self):
        self.game = Game()
        # Simula uma janela ampliada para testar a conversão das coordenadas.
        self.window = SimpleNamespace(
            screen=pygame.Surface((800, 600)),
            screen_to_virtual_coords=lambda x, y: (x / 2, y / 2),
        )

    def click(self, position, page='multiplayer'):
        event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=1,
                                   pos=tuple(value * 2 for value in position))
        buttons = {'rules': RULES_BUTTONS, 'ai_easy': AI_BUTTONS,
                   'ai_levels': AI_LEVEL_BUTTONS, 'modes': MODE_BUTTONS}.get(page, MULTIPLAYER_BUTTONS)
        return handle_event(self.window, event, page, buttons, None,
                            'multiplayer', self.game)

    def square(self, row, col, page='multiplayer'):
        return self.click((BOARD.x + col * SQUARE_SIZE + 26,
                           BOARD.y + row * SQUARE_SIZE + 26), page)

    def test_moves_capture_and_render(self):
        for row, col in [(6, 4), (4, 4), (1, 3), (3, 3), (4, 4), (3, 3)]:
            self.square(row, col)
        self.assertIsNone(self.game.get_piece(4, 4))
        self.assertEqual(self.game.get_piece(3, 3).color, Color.WHITE)
        self.assertEqual(self.game.current_turn, Color.BLACK)
        draw(self.window, 'multiplayer', MULTIPLAYER_BUTTONS, None,
             'home', self.game)

    def test_invalid_move_and_rules_do_not_change_board(self):
        self.square(6, 4)
        self.square(3, 4)
        self.assertIsNotNone(self.game.get_piece(6, 4))
        self.assertEqual(self.game.current_turn, Color.WHITE)
        self.square(4, 4, 'rules')
        self.assertIsNone(self.game.get_piece(4, 4))
        draw(self.window, 'rules', RULES_BUTTONS, None, 'multiplayer', self.game)
        self.assertEqual(self.click(RULES_BUTTONS[0].rect.center, 'rules')[0],
                         'multiplayer')
        self.square(4, 4)
        self.assertEqual(self.game.current_turn, Color.BLACK)

    def test_promotion_popup_and_click(self):
        self.game.board.grid = [[None] * 8 for _ in range(8)]
        self.game.board.set_piece(1, 0, Pawn(Color.WHITE))
        self.square(1, 0)
        self.square(0, 0)
        self.assertIsNotNone(self.game.pending_promotion_move)
        draw(self.window, 'multiplayer', MULTIPLAYER_BUTTONS, None,
             'home', self.game)
        self.click(PROMOTION_OPTIONS[1][1].rect.center)
        self.assertIsInstance(self.game.get_piece(0, 0), Rook)
        self.assertIsNone(self.game.pending_promotion_move)
        self.assertEqual(self.game.current_turn, Color.BLACK)

    def test_ai_menu_and_disabled_levels(self):
        self.assertEqual(self.click(MODE_BUTTONS[2].rect.center, 'modes')[0], 'ai_levels')
        self.assertEqual(self.click(AI_LEVEL_BUTTONS[1].rect.center, 'ai_levels')[0], 'ai_easy')
        for button in AI_LEVEL_BUTTONS[2:]:
            self.assertEqual(self.click(button.rect.center, 'ai_levels')[0], 'ai_levels')
        self.assertEqual(self.click(AI_BUTTONS[0].rect.center, 'ai_easy')[0], 'ai_levels')
        for page, buttons in [('ai_levels', AI_LEVEL_BUTTONS), ('ai_easy', AI_BUTTONS)]:
            draw(self.window, page, buttons, None, 'home', self.game)
        draw(self.window, 'rules', RULES_BUTTONS, None, 'ai_easy', self.game)

    def test_ai_responds_only_after_valid_move(self):
        with patch.object(self.game, 'play_ai_turn', wraps=self.game.play_ai_turn):
            self.square(6, 4, 'ai_easy')
            self.square(3, 4, 'ai_easy')
            self.assertEqual(self.game.current_turn, Color.WHITE)
            self.square(4, 4, 'ai_easy')
            self.assertEqual(self.game.current_turn, Color.BLACK)
            elapsed = update_ai(self.game, 'ai_easy', 0, 799)
            self.assertEqual(self.game.current_turn, Color.BLACK)
            update_ai(self.game, 'ai_easy', elapsed, 1)
        self.assertEqual(self.game.current_turn, Color.WHITE)
        self.assertIsNotNone(self.game.get_piece(4, 4))
        black_positions = [(row, col) for row in range(2, 8) for col in range(8)
                           if self.game.get_piece(row, col) is not None
                           and self.game.get_piece(row, col).color is Color.BLACK]
        self.assertEqual(len(black_positions), 1)

    def test_ai_waits_for_promotion_and_blocks_black_input(self):
        self.game.board.grid = [[None] * 8 for _ in range(8)]
        self.game.board.set_piece(1, 0, Pawn(Color.WHITE))
        self.game.board.set_piece(1, 7, Pawn(Color.BLACK))
        self.square(1, 0, 'ai_easy')
        with patch.object(self.game, 'play_ai_turn', wraps=self.game.play_ai_turn) as reply:
            self.square(0, 0, 'ai_easy')
            reply.assert_not_called()
            self.click(PROMOTION_OPTIONS[1][1].rect.center, 'ai_easy')
            reply.assert_not_called()
            update_ai(self.game, 'ai_easy', 0, 800)
            reply.assert_called_once()
        self.assertIsInstance(self.game.get_piece(0, 0), Rook)
        self.assertEqual(self.game.current_turn, Color.WHITE)
        self.game.current_turn = Color.BLACK
        self.square(0, 0, 'ai_easy')
        self.assertIsNone(self.game.selected_square)

    def test_ai_timer_pauses_in_menus_and_does_not_repeat_without_moves(self):
        self.game.board.grid = [[None] * 8 for _ in range(8)]
        self.game.current_turn = Color.BLACK
        with patch.object(self.game, 'play_ai_turn', wraps=self.game.play_ai_turn) as reply:
            elapsed = update_ai(self.game, 'ai_easy', 0, 400)
            elapsed = update_ai(self.game, 'rules', elapsed, 2000)
            self.assertEqual(elapsed, 400)
            reply.assert_not_called()
            elapsed = update_ai(self.game, 'ai_easy', elapsed, 400)
            update_ai(self.game, 'ai_easy', elapsed, 1000)
            reply.assert_called_once()

    def test_ai_animation_blocks_clicks_pauses_and_finishes(self):
        self.square(6, 4, 'ai_easy')
        self.square(4, 4, 'ai_easy')
        animation = MoveAnimation()
        update_ai(self.game, 'ai_easy', 0, 800, animation)
        self.assertTrue(animation.active)
        update_ai(self.game, 'ai_easy', 0, 175, animation)
        update_ai(self.game, 'rules', 0, 2000, animation)
        self.assertEqual(animation.elapsed_ms, 175)
        draw(self.window, 'ai_easy', AI_BUTTONS, None, 'home', self.game, animation)
        event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=1,
                                   pos=((BOARD.x + 26) * 2, (BOARD.y + 6 * 52 + 26) * 2))
        handle_event(self.window, event, 'ai_easy', AI_BUTTONS, None,
                     'home', self.game, animation)
        self.assertIsNone(self.game.selected_square)
        update_ai(self.game, 'ai_easy', 0, 175, animation)
        self.assertFalse(animation.active)
        handle_event(self.window, event, 'ai_easy', AI_BUTTONS, None,
                     'home', self.game, animation)
        self.assertEqual(self.game.selected_square, (6, 0))

    def test_castling_animation_moves_king_and_rook(self):
        animation = MoveAnimation()
        animation.start(self.game.board.copy(),
                        Move((0, 4), (0, 6), is_castling=True))
        animation.advance(175)
        with patch('interface.components.draw_board.draw_piece') as paint:
            draw_board(self.window.screen, self.game, animation=animation)
        self.assertEqual(paint.call_args_list[-2].args[1:],
                         ('king', 'black', (478, 122)))
        self.assertEqual(paint.call_args_list[-1].args[1:],
                         ('rook', 'black', (530, 122)))

    def test_ai_promotion_animates_pawn_before_showing_queen(self):
        self.game.board.grid = [[None] * 8 for _ in range(8)]
        self.game.board.set_piece(6, 0, Pawn(Color.BLACK))
        self.game.current_turn = Color.BLACK
        animation = MoveAnimation()
        update_ai(self.game, 'ai_easy', 0, 800, animation)
        self.assertIsInstance(animation.board.get_piece(6, 0), Pawn)
        self.assertEqual(type(self.game.get_piece(7, 0)).__name__, 'Queen')
        self.assertTrue(animation.active)

    def test_exit_confirmation_cancel_and_reset_in_both_modes(self):
        for mode, buttons, destination in [('multiplayer', MULTIPLAYER_BUTTONS, 'modes'),
                                            ('ai_easy', AI_BUTTONS, 'ai_levels')]:
            self.game = Game()
            escape = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_ESCAPE)
            self.assertEqual(handle_event(self.window, escape, mode, buttons, None,
                                          'home', self.game)[0], destination)
            self.game.handle_click(6, 4)
            self.game.handle_click(4, 4)
            self.assertEqual(self.game.move_count, 1)
            self.assertEqual(handle_event(self.window, escape, mode, buttons, None,
                                          'home', self.game)[0], 'confirm_exit')
            self.assertEqual(self.click(buttons[0].rect.center, mode)[0], 'confirm_exit')
            draw(self.window, 'confirm_exit', EXIT_BUTTONS, 0, mode, self.game)
            self.assertEqual(handle_event(self.window, escape, 'confirm_exit', EXIT_BUTTONS,
                                          0, mode, self.game)[0], mode)
            self.assertIsNotNone(self.game.get_piece(4, 4))
            enter = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN)
            self.assertEqual(handle_event(self.window, enter, 'confirm_exit', EXIT_BUTTONS,
                                          0, mode, self.game)[0], mode)
            animation = MoveAnimation()
            animation.start(self.game.board.copy(), Move((1, 0), (2, 0)))
            self.assertEqual(handle_event(self.window, enter, 'confirm_exit', EXIT_BUTTONS,
                                          1, mode, self.game, animation)[0], destination)
            self.assertEqual(self.game.move_count, 0)
            self.assertIsNone(self.game.get_piece(4, 4))
            self.assertIsInstance(self.game.get_piece(6, 4), Pawn)
            if mode == 'ai_easy':
                self.assertFalse(animation.active)
