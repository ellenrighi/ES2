import pygame

from interface.components.exit_popup import draw_exit_popup
from interface.components.promotion_popup import draw_promotion_popup
from interface.components.draw_button import draw_button
from interface.components.rules_popup import draw_rules_popup
from interface.screens.home import HOME_BUTTONS, draw_home
from interface.screens.modes import draw_modes
from interface.screens.ai_levels import draw_ai_levels
from interface.screens.multiplayer import AI_BUTTONS, MULTIPLAYER_BUTTONS, draw_multiplayer
from interface.theme import BACKGROUND


def draw(window, page, buttons, focused, rules_parent='home', game=None, animation=None):
    surface = window.screen
    surface.fill(BACKGROUND)
    background_page = rules_parent if page in ('rules', 'confirm_exit') else page
    if background_page == 'multiplayer':
        draw_multiplayer(surface, game)
    elif background_page == 'ai_easy':
        draw_multiplayer(surface, game, 'Vs IA · Fácil', animation)
    elif background_page == 'ai_levels':
        draw_ai_levels(surface)
    elif background_page == 'modes':
        draw_modes(surface)
    else:
        draw_home(surface)
    if page in ('rules', 'confirm_exit'):
        # A tela anterior continua visível, mas só o pop-up recebe interações.
        background_buttons = {'multiplayer': MULTIPLAYER_BUTTONS,
                              'ai_easy': AI_BUTTONS}.get(rules_parent, HOME_BUTTONS)
        for button in background_buttons:
            draw_button(button, surface, (-1, -1), False)
        if page == 'rules':
            draw_rules_popup(surface)
        else:
            draw_exit_popup(surface)
    mouse = window.screen_to_virtual_coords(*pygame.mouse.get_pos())
    for i, button in enumerate(buttons):
        draw_button(button, surface, mouse, focused == i)

    if page in ('multiplayer', 'ai_easy') and game.pending_promotion_move is not None:
        draw_promotion_popup(surface)
