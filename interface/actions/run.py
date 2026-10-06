import pygame

from PPlay.window import Window
from src.application.game import Game
from interface.actions.draw import draw
from interface.actions.handle_event import handle_event
from interface.components.rules_popup import RULES_BUTTONS
from interface.screens.home import HOME_BUTTONS
from interface.screens.modes import MODE_BUTTONS
from interface.screens.multiplayer import MULTIPLAYER_BUTTONS


def run():
    try:
        window = Window(800, 600, 'Xadrez', pixel_art=False)
        page, focused = 'home', None
        rules_parent = 'home'
        game = Game()
        buttons = {'home': HOME_BUTTONS, 'modes': MODE_BUTTONS,
                   'multiplayer': MULTIPLAYER_BUTTONS, 'rules': RULES_BUTTONS}
        clock = pygame.time.Clock()
        while True:
            for event in window.eventos:
                next_page, focused = handle_event(window, event, page, buttons[page], focused, rules_parent, game)
                if next_page == 'rules' and page != 'rules':
                    rules_parent = page
                page = next_page
            draw(window, page, buttons[page], focused, rules_parent, game)
            window.update()
            clock.tick(60)
    finally:
        pygame.quit()
