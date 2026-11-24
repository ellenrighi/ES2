import pygame

from interface.drawing.font import font
from interface.drawing.load_icon import load_icon
from interface.theme import ACCENT, TEXT
from src.domain.color import Color


def draw_result_popup(surface, winner, elapsed_ms, reason=None):
    progress = min(elapsed_ms / 650, 1)
    entrance = 1 - (1 - progress) ** 3
    overlay = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
    overlay.fill((15, 75, 43, round(192 * entrance)))
    surface.blit(overlay, (0, 0))

    center_x, center_y = surface.get_rect().center
    if winner is None:
        title_text = 'Empate'
    else:
        title_text = 'Brancas venceram' if winner is Color.WHITE else 'Pretas venceram'
    title_font = font(52, True)
    title_width, title_height = title_font.size(title_text)
    title_left = center_x - title_width // 2
    title_offset = 24 if reason else 0
    title_top = center_y - title_offset - title_height // 2
    if winner is not None:
        trophy = load_icon('trophy.png').copy()
        trophy.set_alpha(round(255 * entrance))
        surface.blit(trophy, trophy.get_rect(midbottom=(center_x, title_top - 12)))

    for index, character in enumerate(title_text):
        letter_elapsed_ms = elapsed_ms - 80 - index * 36
        if letter_elapsed_ms <= 0:
            break
        if character == ' ':
            continue
        letter = title_font.render(character, True, TEXT)
        letter.set_alpha(round(255 * min(letter_elapsed_ms / 190, 1)))
        prefix_width, _ = title_font.size(title_text[:index + 1])
        letter_left = title_left + prefix_width - letter.get_width()
        surface.blit(letter, (letter_left, title_top))

    if reason and elapsed_ms >= 1050:
        reveal = min((elapsed_ms - 1050) / 450, 1)
        subtitle = font(24, True).render(reason, True, ACCENT)
        subtitle.set_alpha(round(255 * reveal))
        surface.blit(subtitle, subtitle.get_rect(center=(center_x, center_y + 33)))
