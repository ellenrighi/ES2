from interface.drawing.load_icon import load_icon


def draw_piece(surface, piece, side, center):
    image = load_icon(f'pieces/{side}-{piece}.png')
    surface.blit(image, image.get_rect(center=center))
