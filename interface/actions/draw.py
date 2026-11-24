import pygame

from interface.components.draw_board import draw_board
from interface.components.exit_popup import draw_exit_popup
from interface.components.promotion_popup import draw_promotion_popup
from interface.components.draw_button import draw_button
from interface.components.result_popup import draw_result_popup
from interface.components.rules_popup import draw_rules_popup
from interface.screens.home import HOME_BUTTONS, draw_home
from interface.screens.modes import draw_modes
from interface.screens.ai_levels import AI_LEVELS, draw_ai_levels
from interface.screens.multiplayer import AI_BUTTONS, MULTIPLAYER_BUTTONS, draw_multiplayer
from interface.theme import BACKGROUND
from src.domain.color import Color


def draw(window, page, buttons, focused, rules_parent='home', game=None, animation=None,
         result_elapsed_ms=0, result_reason=None):
    surface = window.screen
    surface.fill(BACKGROUND)
    if page == 'result':
        draw_board(surface, game)
        defeat = rules_parent in AI_LEVELS and game.winner is Color.BLACK
        draw_result_popup(surface, game.winner, result_elapsed_ms, reason=result_reason,
                          defeat=defeat)
        return
    popup_open = page in ('rules', 'confirm_exit')
    background_page = rules_parent if popup_open else page
    if background_page == 'multiplayer':
        draw_multiplayer(surface, game)
    elif background_page in AI_LEVELS:
        _, label = AI_LEVELS[background_page]
        draw_multiplayer(surface, game, f'Vs IA · {label}', animation)
    elif background_page == 'ai_levels':
        draw_ai_levels(surface)
    elif background_page == 'modes':
        draw_modes(surface)
    else:
        draw_home(surface)
    if popup_open:
        # A tela anterior continua visível, mas só o pop-up recebe interações.
        if background_page in AI_LEVELS:
            background_buttons = AI_BUTTONS
        elif background_page == 'multiplayer':
            background_buttons = MULTIPLAYER_BUTTONS
        else:
            background_buttons = HOME_BUTTONS
        for button in background_buttons:
            draw_button(button, surface, (-1, -1), False)
        if page == 'rules':
            draw_rules_popup(surface)
        else:
            draw_exit_popup(surface)
    mouse = window.screen_to_virtual_coords(*pygame.mouse.get_pos())
    for i, button in enumerate(buttons):
        draw_button(button, surface, mouse, focused == i)

    if (page == 'multiplayer' or page in AI_LEVELS) and game.pending_promotion_move is not None:
        draw_promotion_popup(surface)
