import pygame

from interface.components.button import Button
from interface.drawing.font import font
from interface.theme import ACCENT, MUTED, PANEL, TEXT

RULES_BUTTONS = [Button(pygame.Rect(648, 55, 44, 44), '×', 'home')]

# Resumo das regras básicas: https://handbook.fide.com/chapter/E012023
RULES = [
    ('Objetivo', (
        'Dê xeque-mate: ataque o rei adversário sem que ele possa escapar.',
        'Você nunca pode deixar seu próprio rei em xeque.',
    )),
    ('Turnos e capturas', (
        'As brancas começam. Os jogadores alternam um lance por vez.',
        'Ao capturar, a peça adversária é retirada do tabuleiro.',
    )),
    ('Movimento das peças', (
        'Torre: retas. Bispo: diagonais. Dama: retas e diagonais.',
        'Rei: uma casa. Cavalo: em L, podendo saltar outras peças.',
    )),
    ('Peões e promoção', (
        'Avançam uma casa, ou duas no primeiro lance, se o caminho estiver livre.',
        'Capturam na diagonal. Na última fileira, viram dama, torre, bispo ou cavalo.',
    )),
    ('Lances especiais', (
        'Roque: movimento conjunto do rei e de uma torre, sob condições específicas.',
        'En passant: captura especial de peão logo após o avanço duplo de um rival.',
    )),
    ('Empate', (
        'Sem lance legal e sem estar em xeque, ocorre afogamento: a partida empata.',
        'Também há empate quando nenhum dos lados pode dar xeque-mate.',
    )),
]


def draw_rules_popup(surface):
    overlay = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 155))
    surface.blit(overlay, (0, 0))
    pygame.draw.rect(surface, PANEL, (80, 35, 640, 530), border_radius=18)
    pygame.draw.rect(surface, '#405045', (80, 35, 640, 530), 1, 18)
    surface.blit(font(28, True).render('Regras do xadrez', True, TEXT), (108, 61))
    pygame.draw.line(surface, '#405045', (108, 108), (692, 108))
    for index, (title, lines) in enumerate(RULES):
        y = 123 + index * 64
        surface.blit(font(17, True).render(title, True, ACCENT), (108, y))
        for line_index, line in enumerate(lines):
            surface.blit(font(15).render(line, True, TEXT), (108, y + 23 + line_index * 19))
    surface.blit(font(13).render('Resumo das regras · Esc para fechar', True, MUTED), (108, 534))
