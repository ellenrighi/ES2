import pygame

from interface.drawing.centered_text import centered_text
from interface.theme import ACCENT, PANEL
from src.domain.color import Color

def draw_victory_popup(surface, winner):
    overlay = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 155))
    surface.blit(overlay, (0, 0))
    pygame.draw.rect(surface, PANEL, (170, 232, 460, 136), border_radius=18)
    centered_text(surface, 'Xeque-mate', 256, 18, color=ACCENT, bold=True)
    title = 'Brancas venceram' if winner is Color.WHITE else 'Pretas venceram'
    centered_text(surface, title, 287, 32, bold=True)
