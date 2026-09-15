import pygame


def handle_event(window, event, page, buttons, focused, rules_parent='home'):
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
