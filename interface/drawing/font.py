from functools import lru_cache

import pygame


@lru_cache(maxsize=32)
def font(size, bold=False):
    return pygame.font.SysFont('arial', size, bold=bold)
