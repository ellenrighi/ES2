import pygame

from interface.components.button import Button
from interface.drawing.centered_text import centered_text

AI_LEVEL_BUTTONS = [
    Button(pygame.Rect(48, 40, 48, 48), 'Voltar', 'modes', icon='arrow-left.png'),
    Button(pygame.Rect(250, 230, 300, 52), 'Fácil', 'ai_easy'),
    Button(pygame.Rect(250, 298, 300, 52), 'Médio', enabled=False),
    Button(pygame.Rect(250, 366, 300, 52), 'Difícil', enabled=False),
]


def draw_ai_levels(surface):
    centered_text(surface, 'Escolha a dificuldade', 140, 30, bold=True)
    centered_text(surface, 'Você joga com as brancas. A IA joga com as pretas.', 190, 17)
