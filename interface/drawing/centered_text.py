from interface.drawing.font import font
from interface.theme import TEXT


def centered_text(surface, value, y, size=18, color=TEXT, bold=False):
    label = font(size, bold).render(value, True, color)
    surface.blit(label, label.get_rect(midtop=(surface.get_width() // 2, y)))
