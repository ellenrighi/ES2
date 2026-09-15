from functools import lru_cache

import pygame

from interface.paths import KING_IMAGE
from interface.theme import BACKGROUND, PANEL


@lru_cache(maxsize=1)
def chess_decoration():
    """Pequeno tabuleiro com um rei, apenas para decorar o menu."""
    illustration = pygame.Surface((360, 360), pygame.SRCALPHA)
    pygame.draw.rect(illustration, PANEL, (0, 0, 360, 360), border_radius=20)
    for row in range(8):
        for column in range(8):
            color = '#87977B' if (row + column) % 2 == 0 else '#405744'
            pygame.draw.rect(illustration, color, (20 + column * 40, 20 + row * 40, 40, 40))

    king = pygame.image.load(str(KING_IMAGE)).convert_alpha()
    shadow = pygame.mask.from_surface(king).to_surface(
        setcolor=pygame.Color(BACKGROUND), unsetcolor=(0, 0, 0, 0))
    illustration.blit(shadow, (63, 65))
    illustration.blit(king, (60, 60))
    return pygame.transform.smoothscale(illustration, (180, 180))
