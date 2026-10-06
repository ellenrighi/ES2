import pygame

from interface.components.draw_board import BOARD, SQUARE_SIZE
from interface.components.promotion_popup import PROMOTION_OPTIONS


def handle_event(window, event, page, buttons, focused, rules_parent='home', game=None):
    if page == 'multiplayer' and game is not None:
        if game.pending_promotion_move is not None:
            code = None
            if event.type == pygame.KEYDOWN:
                code = {pygame.K_q: 'Q', pygame.K_r: 'R',
                        pygame.K_b: 'B', pygame.K_n: 'N'}.get(event.key)
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                position = window.screen_to_virtual_coords(*event.pos)
                code = next((code for code, button in PROMOTION_OPTIONS
                             if button.rect.collidepoint(position)), None)
            if code:
                game.choose_promotion(code)
            return page, None
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            position = window.screen_to_virtual_coords(*event.pos)
            if BOARD.collidepoint(position):
                column = int((position[0] - BOARD.x) // SQUARE_SIZE)
                row = int((position[1] - BOARD.y) // SQUARE_SIZE)
                game.handle_click(row, column)
                return page, None

    selected = None
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE and page == 'rules':
            return rules_parent, None
        elif event.key == pygame.K_ESCAPE and page == 'multiplayer':
            return 'modes', None
        elif event.key == pygame.K_ESCAPE and page == 'modes':
            return 'home', None
        elif event.key == pygame.K_TAB:
            enabled = [i for i, button in enumerate(buttons) if button.enabled]
            step = -1 if event.mod & pygame.KMOD_SHIFT else 1
            if focused in enabled:
                focused = enabled[(enabled.index(focused) + step) % len(enabled)]
            elif enabled:
                focused = enabled[0 if step == 1 else -1]
        elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
            selected = focused
    elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
        position = window.screen_to_virtual_coords(*event.pos)
        for i, button in enumerate(buttons):
            if button.rect.collidepoint(position):
                selected = i
                break

    if selected is not None:
        button = buttons[selected]
        if button.enabled:
            if button.is_toggle:
                button.checked = not button.checked
            elif button.action == 'close_rules':
                return rules_parent, None
            elif button.action:
                return button.action, None
    return page, focused
