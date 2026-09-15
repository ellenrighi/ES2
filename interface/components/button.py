from dataclasses import dataclass, field

import pygame


@dataclass
class Button:
    """Dados de um botão; o desenho fica em draw_button.py."""

    rect: pygame.Rect
    label: str
    action: str = ''
    enabled: bool = True
    primary: bool = False
    icon: str = ''
    is_toggle: bool = False
    checked: bool = False
    toggle_progress: float = field(default=0, init=False, repr=False)
    hover_progress: float = field(default=0, init=False, repr=False)
    hover_updated_at: int = field(default=0, init=False, repr=False)
