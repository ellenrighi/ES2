import pygame

from PPlay.window import Window
from src.application.game import Game
from src.domain.color import Color
from src.domain.piece import Bishop, King, Knight, Pawn, Queen, Rook


class ChessGUI:
    """Controla a interface grafica da partida de xadrez.

    Parametros:
        Nenhum.
    Retorno:
        Instancia de ``ChessGUI`` pronta para desenhar e receber entradas.
    """

    BOARD_PIXELS = 640
    CELL_SIZE = BOARD_PIXELS // 8
    PANEL_WIDTH = 260
    WIDTH = BOARD_PIXELS + PANEL_WIDTH
    HEIGHT = BOARD_PIXELS

    #Cor dos quadriculados
    LIGHT = (139, 90, 43)
    DARK = (92, 64, 51)
    #Cores de destaque
    HIGHLIGHT = (246, 246, 105)
    TARGET = (186, 202, 68)
    #MISC
    BACKGROUND = (0, 0, 0)
    TEXT = (20, 20, 20)
    PANEL_BG = (220, 220, 220)
    #Pecas
    WHITE_PIECE = (245, 245, 245)
    BLACK_PIECE = (10, 10, 10)

    def __init__(self) -> None:
        """Inicializa janela, controles de entrada e estado do jogo.

        Parametros:
            Nenhum.
        Retorno:
            None.
        """
        self.window = Window(self.WIDTH, self.HEIGHT, "Xadrez V1 - IA Aleatória")
        self.game = Game()
        self.mouse = self.window.mouse
        self.keyboard = self.window.keyboard

    def run(self) -> None:
        """Inicia o loop principal de atualizacao da interface.

        Parametros:
            Nenhum.
        Retorno:
            None.
        """
        while True:
            self._handle_input()
            self._draw()
            self.window.update()

    def _handle_input(self) -> None:
        """Processa eventos de mouse e teclado da interface.

        Parametros:
            Nenhum.
        Retorno:
            None.
        """
        if self.mouse.button_down(1):
            mx, my = self.mouse.get_position()
            row = int(my // self.CELL_SIZE)
            col = int(mx // self.CELL_SIZE)
            if 0 <= row < 8 and 0 <= col < 8:
                self.game.handle_click(row, col)
                if self.game.current_turn is Color.BLACK:
                    self.game.play_ai_turn()

        if self.game.pending_promotion_move is not None:
            if self.keyboard.key_down("q"):
                self.game.choose_promotion("Q")
            elif self.keyboard.key_down("r"):
                self.game.choose_promotion("R")
            elif self.keyboard.key_down("b"):
                self.game.choose_promotion("B")
            elif self.keyboard.key_down("n"):
                self.game.choose_promotion("N")

        if self.keyboard.key_down("esc"):
            self.window.close()

    def _draw(self) -> None:
        """Desenha o quadro completo da interface no frame atual.

        Parametros:
            Nenhum.
        Retorno:
            None.
        """
        self.window.set_background_color(self.BACKGROUND)
        self._draw_board()
        self._draw_overlays()
        self._draw_pieces()
        self._draw_panel()

    def _draw_board(self) -> None:
        """Desenha o tabuleiro quadriculado na area principal.

        Parametros:
            Nenhum.
        Retorno:
            None.
        """
        surface = Window.get_screen()
        for row in range(8):
            for col in range(8):
                color = self.LIGHT if (row + col) % 2 == 0 else self.DARK
                rect = pygame.Rect(col * self.CELL_SIZE, row * self.CELL_SIZE, self.CELL_SIZE, self.CELL_SIZE)
                pygame.draw.rect(surface, color, rect)

    def _draw_overlays(self) -> None:
        """Desenha destaque de selecao e destinos de movimentos legais.

        Parametros:
            Nenhum.
        Retorno:
            None.
        """
        surface = Window.get_screen()
        if self.game.selected_square is not None:
            sr, sc = self.game.selected_square
            selected_rect = pygame.Rect(sc * self.CELL_SIZE, sr * self.CELL_SIZE, self.CELL_SIZE, self.CELL_SIZE)
            pygame.draw.rect(surface, self.HIGHLIGHT, selected_rect, 5)

        for (row, col) in self.game.legal_moves_by_dest.keys():
            rect = pygame.Rect(col * self.CELL_SIZE, row * self.CELL_SIZE, self.CELL_SIZE, self.CELL_SIZE)
            pygame.draw.rect(surface, self.TARGET, rect, 4)

    def _draw_pieces(self) -> None:
        """Desenha as pecas atualmente posicionadas no tabuleiro.

        Parametros:
            Nenhum.
        Retorno:
            None.
        """
        for row in range(8):
            for col in range(8):
                piece = self.game.get_piece(row, col)
                if piece is None:
                    continue
                label = self._piece_label(piece)
                color = self.WHITE_PIECE if piece.color is Color.WHITE else self.BLACK_PIECE
                x = col * self.CELL_SIZE + 22
                y = row * self.CELL_SIZE + 24
                self.window.draw_text(label, x, y, tamanho=28, cor=color, fonte="Arial")

    def _draw_panel(self) -> None:
        """Desenha o painel lateral com status e instrucoes ao jogador.

        Parametros:
            Nenhum.
        Retorno:
            None.
        """
        surface = Window.get_screen()
        panel_x = self.BOARD_PIXELS
        pygame.draw.rect(surface, self.PANEL_BG, pygame.Rect(panel_x, 0, self.PANEL_WIDTH, self.HEIGHT))

        self.window.draw_text("Xadrez V1", panel_x + 20, 20, tamanho=30, cor=self.TEXT)
        self.window.draw_text(self.game.status_message, panel_x + 20, 70, tamanho=20, cor=self.TEXT)
        self.window.draw_text("Clique: selecionar/mover", panel_x + 20, 120, tamanho=18, cor=self.TEXT)
        self.window.draw_text("ESC: sair", panel_x + 20, 150, tamanho=18, cor=self.TEXT)

        if self.game.pending_promotion_move is not None:
            self.window.draw_text("Promocao:", panel_x + 20, 210, tamanho=20, cor=(120, 20, 20))
            self.window.draw_text("Q=Dama R=Torre", panel_x + 20, 240, tamanho=18, cor=(120, 20, 20))
            self.window.draw_text("B=Bispo N=Cavalo", panel_x + 20, 265, tamanho=18, cor=(120, 20, 20))

    @staticmethod
    def _piece_label(piece) -> str:
        """Converte o tipo de peca para o rotulo textual exibido na tela.

        Parametros:
            piece: Instancia da peca a ser rotulada.
        Retorno:
            str: Letra representando a peca, ou ``?`` se desconhecida.
        """
        labels = {
            Pawn: "P",
            Rook: "R",
            Knight: "N",
            Bishop: "B",
            Queen: "Q",
            King: "K",
        }
        return labels.get(type(piece), "?")
