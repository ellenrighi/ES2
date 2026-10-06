import os
os.environ.setdefault('SDL_VIDEODRIVER', 'dummy')
os.environ.setdefault('SDL_AUDIODRIVER', 'dummy')

import unittest
from types import SimpleNamespace

import pygame

from interface.actions.draw import draw
from interface.actions.handle_event import handle_event
from interface.components.draw_board import BOARD, SQUARE_SIZE
from interface.components.promotion_popup import PROMOTION_OPTIONS
from interface.components.rules_popup import RULES_BUTTONS
from interface.screens.multiplayer import MULTIPLAYER_BUTTONS
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
        buttons = RULES_BUTTONS if page == 'rules' else MULTIPLAYER_BUTTONS
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
