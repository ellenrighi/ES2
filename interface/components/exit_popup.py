import pygame

from interface.components.button import Button
from interface.drawing.centered_text import centered_text
from interface.theme import PANEL

EXIT_BUTTONS = [
    Button(pygame.Rect(176, 326, 208, 48), 'Continuar jogando', 'cancel_exit'),
    Button(pygame.Rect(408, 326, 216, 48), 'Sair e reiniciar', 'confirm_exit', primary=True),
]


def draw_exit_popup(surface):
    overlay = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 155))
    surface.blit(overlay, (0, 0))
    pygame.draw.rect(surface, PANEL, (128, 210, 544, 190), border_radius=18)
    centered_text(surface, 'Deseja sair e reiniciar o jogo?', 250, 25, bold=True)
    centered_text(surface, 'O progresso desta partida será perdido.', 290, 17)
