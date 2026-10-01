from __future__ import annotations

from src.domain.board import Board
from src.domain.color import Color
from src.domain.move import Move
from src.domain.piece import Piece
from src.ai.random_ai import choose_random_move


class Game:
    """Orquestra o fluxo da partida e estado da interacao do jogador.

    Parametros:
        Nenhum.
    Retorno:
        Instancia de ``Game`` pronta para iniciar uma partida.
    """

    def __init__(self) -> None:
        """Inicializa tabuleiro, turno, selecao e mensagens de estado.

        Parametros:
            Nenhum.
        Retorno:
            None.
        """
        self.board = Board()
        self.current_turn = Color.WHITE
        self.selected_square: tuple[int, int] | None = None
        self.legal_moves_by_dest: dict[tuple[int, int], Move] = {}
        self.pending_promotion_move: Move | None = None
        self.status_message = "Turno: Brancas"

    def get_piece(self, row: int, col: int) -> Piece | None:
        """Obtém a peca em uma coordenada do tabuleiro.

        Parametros:
            row (int): Linha desejada.
            col (int): Coluna desejada.
        Retorno:
            Piece | None: Peca encontrada ou ``None``.
        """
        return self.board.get_piece(row, col)

    def handle_click(self, row: int, col: int) -> None:
        """Processa um clique do usuario no tabuleiro.

        Parametros:
            row (int): Linha clicada.
            col (int): Coluna clicada.
        Retorno:
            None.
        """
        if self.pending_promotion_move is not None:
            self.status_message = "Escolha promocao: Q, R, B ou N."
            return

        piece = self.board.get_piece(row, col)

        if self.selected_square is None:
            if piece is None:
                self.status_message = self._turn_text()
                return
            if piece.color is not self.current_turn:
                self.status_message = "Selecione uma peca do turno atual."
                return
            self._select_piece(row, col)
            return

        if piece is not None and piece.color is self.current_turn:
            self._select_piece(row, col)
            return

        target = (row, col)
        move = self.legal_moves_by_dest.get(target)
        if move is None:
            self.status_message = "Movimento invalido."
            return

        if move.requires_promotion:
            self.pending_promotion_move = move
            self.status_message = "Escolha promocao: Q, R, B ou N."
            return

        self._execute_and_advance(move)

    def choose_promotion(self, promotion_piece: str) -> None:
        """Define a peca de promocao pendente e conclui o movimento.

        Parametros:
            promotion_piece (str): Codigo da peca escolhida (Q, R, B ou N).
        Retorno:
            None.
        """
        if self.pending_promotion_move is None:
            return
        code = promotion_piece.upper()
        if code not in {"Q", "R", "B", "N"}:
            self.status_message = "Promocao invalida. Use Q, R, B ou N."
            return
        move = self.pending_promotion_move
        move.promotion_piece = code
        self.pending_promotion_move = None
        self._execute_and_advance(move)

    def _select_piece(self, row: int, col: int) -> None:
        """Seleciona uma peca e calcula seus movimentos possiveis.

        Parametros:
            row (int): Linha da peca selecionada.
            col (int): Coluna da peca selecionada.
        Retorno:
            None.
        """
        self.selected_square = (row, col)
        legal_moves = self.board.generate_moves_for_piece(row, col)
        self.legal_moves_by_dest = {m.end_pos: m for m in legal_moves}
        self.status_message = f"{self._piece_name(self.board.get_piece(row, col))} selecionada."
    def play_ai_turn(self) -> None:
        if self.current_turn is not Color.BLACK:
             return

        move = choose_random_move(self.board, Color.BLACK)

        if move is None:
            self.status_message = "A IA não possui movimentos disponíveis."
            return

        self._execute_and_advance(move)

    def _execute_and_advance(self, move: Move) -> None:
        """Executa um movimento valido e alterna o turno.

        Parametros:
            move (Move): Movimento legal que sera aplicado.
        Retorno:
            None.
        """
        self.board.execute_move(move)
        self.selected_square = None
        self.legal_moves_by_dest = {}
        self.current_turn = self.current_turn.opposite()
        self.status_message = self._turn_text()

    def _turn_text(self) -> str:
        """Gera o texto de interface para o turno atual.

        Parametros:
            Nenhum.
        Retorno:
            str: Mensagem com o jogador da vez.
        """
        return "Turno: Brancas" if self.current_turn is Color.WHITE else "Turno: Pretas"

    @staticmethod
    def _piece_name(piece: Piece | None) -> str:
        """Retorna um nome amigavel para a peca informada.

        Parametros:
            piece (Piece | None): Peca para extrair o nome.
        Retorno:
            str: Nome da classe da peca, ou valor generico quando vazio.
        """
        if piece is None:
            return "Peca"
        return type(piece).__name__
