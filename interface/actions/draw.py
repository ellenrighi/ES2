import pygame

from interface.components.draw_button import draw_button
from interface.components.rules_popup import draw_rules_popup
from interface.screens.home import HOME_BUTTONS, draw_home
from interface.screens.modes import draw_modes
from interface.theme import BACKGROUND


def draw(window, page, buttons, focused):
    surface = window.screen
    surface.fill(BACKGROUND)
    if page == 'modes':
        draw_modes(surface)
    else:
        draw_home(surface)
    if page == 'rules':
        # O menu continua visível, mas só o pop-up recebe interações.
        for button in HOME_BUTTONS:
            draw_button(button, surface, (-1, -1), False)
        draw_rules_popup(surface)
    mouse = window.screen_to_virtual_coords(*pygame.mouse.get_pos())
    for i, button in enumerate(buttons):
        draw_button(button, surface, mouse, focused == i)
