import pygame

from interface.components.button import Button
from interface.drawing.centered_text import centered_text
from src.ai.difficulty import Difficulty

AI_LEVELS = {
    'ai_easy': (Difficulty.EASY, 'Fácil'),
    'ai_medium': (Difficulty.MEDIUM, 'Médio'),
}

AI_LEVEL_BUTTONS = [
    Button(pygame.Rect(48, 40, 48, 48), 'Voltar', 'modes', icon='arrow-left.png'),
    *(Button(pygame.Rect(250, 230 + index * 68, 300, 52), label, page)
      for index, (page, (_, label)) in enumerate(AI_LEVELS.items())),
]


def draw_ai_levels(surface):
    centered_text(surface, 'Escolha a dificuldade', 140, 30, bold=True)
    centered_text(surface, 'Você joga com as brancas. A IA joga com as pretas.', 190, 17)
