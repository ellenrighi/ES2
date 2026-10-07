import pygame

from interface.components.button import Button
from interface.drawing.centered_text import centered_text

MODE_BUTTONS = [
    Button(pygame.Rect(48, 40, 48, 48), 'Voltar', 'home', icon='arrow-left.png'),
    Button(pygame.Rect(250, 240, 300, 52), 'Multiplayer', 'multiplayer'),
    Button(pygame.Rect(250, 308, 300, 52), 'Vs IA', 'ai_levels'),
]

def draw_modes(surface):
    centered_text(surface, 'Escolha o modo de jogo', 160, 30, bold=True)
