import pygame

from PPlay.window import Window
from src.application.game import Game
from interface.components.move_animation import MoveAnimation
from interface.actions.draw import draw
from interface.actions.update_ai import update_ai
from interface.actions.handle_event import handle_event
from interface.components.exit_popup import EXIT_BUTTONS
from interface.components.rules_popup import RULES_BUTTONS
from interface.screens.home import HOME_BUTTONS
from interface.screens.modes import MODE_BUTTONS
from interface.screens.ai_levels import AI_LEVEL_BUTTONS
from interface.screens.multiplayer import AI_BUTTONS, MULTIPLAYER_BUTTONS


def run():
    try:
        window = Window(800, 600, 'Xadrez', pixel_art=False)
        page, focused = 'home', None
        rules_parent = 'home'
        games = {'multiplayer': Game(), 'ai_easy': Game()}
        buttons = {'home': HOME_BUTTONS, 'modes': MODE_BUTTONS,
                   'multiplayer': MULTIPLAYER_BUTTONS, 'rules': RULES_BUTTONS,
                   'ai_levels': AI_LEVEL_BUTTONS, 'ai_easy': AI_BUTTONS,
                   'confirm_exit': EXIT_BUTTONS}
        clock = pygame.time.Clock()
        ai_elapsed_ms = 0
        animation = MoveAnimation()
        while True:
            delta_ms = clock.tick(60)
            for event in window.eventos:
                game = games.get(rules_parent if page in ('rules', 'confirm_exit') else page)
                next_page, focused = handle_event(window, event, page, buttons[page], focused, rules_parent, game, animation)
                if next_page in ('rules', 'confirm_exit') and page not in ('rules', 'confirm_exit'):
                    rules_parent = page
                page = next_page
            ai_elapsed_ms = update_ai(games['ai_easy'], page, ai_elapsed_ms, delta_ms, animation)
            game = games.get(rules_parent if page in ('rules', 'confirm_exit') else page)
            draw(window, page, buttons[page], focused, rules_parent, game, animation)
            window.update()
    finally:
        pygame.quit()
