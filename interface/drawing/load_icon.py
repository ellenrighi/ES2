from functools import lru_cache
import pygame
from interface.paths import ASSETS

@lru_cache(maxsize=32)
def load_icon(name):
    return pygame.image.load(str(ASSETS / 'icons' / name)).convert_alpha()
