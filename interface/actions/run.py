import pygame

from PPlay.window import Window
from interface.actions.draw import draw
from interface.actions.handle_event import handle_event
from interface.components.rules_popup import RULES_BUTTONS
from interface.screens.home import HOME_BUTTONS
from interface.screens.modes import MODE_BUTTONS


def run():
    try:
        window = Window(800, 600, 'Xadrez', pixel_art=False)
        page, focused = 'home', None
        buttons = {'home': HOME_BUTTONS, 'modes': MODE_BUTTONS, 'rules': RULES_BUTTONS}
        clock = pygame.time.Clock()
        while True:
            for event in window.eventos:
                page, focused = handle_event(window, event, page, buttons[page], focused)
            draw(window, page, buttons[page], focused)
            window.update()
            clock.tick(60)
    finally:
        pygame.quit()
