import pygame

from interface.components.draw_button import draw_button
from interface.components.rules_popup import draw_rules_popup
from interface.screens.home import HOME_BUTTONS, draw_home
from interface.screens.modes import draw_modes
from interface.screens.multiplayer import MULTIPLAYER_BUTTONS, draw_multiplayer
from interface.theme import BACKGROUND


def draw(window, page, buttons, focused, rules_parent='home'):
    surface = window.screen
    surface.fill(BACKGROUND)
    background_page = rules_parent if page == 'rules' else page
    if background_page == 'multiplayer':
        draw_multiplayer(surface)
    elif background_page == 'modes':
        draw_modes(surface)
    else:
        draw_home(surface)
    if page == 'rules':
        # A tela anterior continua visível, mas só o pop-up recebe interações.
        background_buttons = MULTIPLAYER_BUTTONS if rules_parent == 'multiplayer' else HOME_BUTTONS
        for button in background_buttons:
            draw_button(button, surface, (-1, -1), False)
        draw_rules_popup(surface)
    mouse = window.screen_to_virtual_coords(*pygame.mouse.get_pos())
    for i, button in enumerate(buttons):
        draw_button(button, surface, mouse, focused == i)
