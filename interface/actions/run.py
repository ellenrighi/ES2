import pygame

from PPlay.window import Window
from src.application.game import Game
from interface.components.move_animation import MoveAnimation
from interface.actions.draw import draw
from interface.actions.update_ai import update_ai
from interface.actions.handle_event import handle_event
from interface.components.exit_popup import EXIT_BUTTONS
from interface.components.result_popup import RESULT_BUTTONS
from interface.components.rules_popup import RULES_BUTTONS
from interface.screens.home import HOME_BUTTONS
from interface.screens.modes import MODE_BUTTONS
from interface.screens.ai_levels import AI_LEVELS, AI_LEVEL_BUTTONS
from interface.screens.multiplayer import AI_BUTTONS, MULTIPLAYER_BUTTONS


def run():
    try:
        window = Window(800, 600, 'Xadrez', pixel_art=False)
        page, focused = 'home', None
        rules_parent = 'home'
        popups = ('rules', 'confirm_exit', 'result')
        games = {'multiplayer': Game(),
                 **{page: Game(difficulty) for page, (difficulty, _) in AI_LEVELS.items()}}
        buttons = {'home': HOME_BUTTONS, 'modes': MODE_BUTTONS,
                   'multiplayer': MULTIPLAYER_BUTTONS, 'rules': RULES_BUTTONS,
                   'ai_levels': AI_LEVEL_BUTTONS, 'confirm_exit': EXIT_BUTTONS,
                   'result': RESULT_BUTTONS,
                   **dict.fromkeys(AI_LEVELS, AI_BUTTONS)}
        clock = pygame.time.Clock()
        ai_elapsed_ms = 0
        result_elapsed_ms = 0
        result_reason = None
        animation = MoveAnimation()
        while True:
            delta_ms = clock.tick(60)
            for event in window.eventos:
                game = games.get(rules_parent if page in popups else page)
                next_page, focused = handle_event(window, event, page, buttons[page], focused, rules_parent, game, animation)
                if next_page in popups and page not in popups:
                    rules_parent = page
                page = next_page
            background_page = rules_parent if page in popups else page
            game = games.get(background_page)
            ai_game = game if background_page in AI_LEVELS else None
            ai_elapsed_ms = update_ai(ai_game, page, ai_elapsed_ms, delta_ms, animation)
            if page == 'result':
                result_elapsed_ms += delta_ms
            elif page in games and game.game_over and not animation.active:
                rules_parent, page, focused = page, 'result', None
                result_elapsed_ms = 0
                result_reason = 'Xeque-mate' if game.winner is not None else None
            draw(window, page, buttons[page], focused, rules_parent, game, animation,
                 result_elapsed_ms=result_elapsed_ms, result_reason=result_reason)
            window.update()
    finally:
        pygame.quit()
