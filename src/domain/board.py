from __future__ import annotations

from .color import Color
from .move import Move
from .piece import Bishop, King, Knight, Pawn, Piece, Queen, Rook


class Board:
    """Representa o tabuleiro e regras de manipulacao de estado da partida.

    Parametros:
        Nenhum.
    Retorno:
        Instancia de ``Board`` inicializada com as pecas na posicao inicial.
    """

    def __init__(self) -> None:
        """Inicializa o tabuleiro, estado de en passant e posicao inicial.

        Parametros:
            Nenhum.
        Retorno:
            None.
        """
        self.grid: list[list[Piece | None]] = [[None for _ in range(8)] for _ in range(8)]
        self.en_passant_target: tuple[int, int] | None = None
        self.setup_initial_position()

    def copy(self) -> "Board":
        """Cria uma copia independente do estado atual do tabuleiro."""
        cloned = Board()
        cloned.grid = [
            [piece.copy() if piece is not None else None for piece in row]
            for row in self.grid
        ]
        cloned.en_passant_target = self.en_passant_target
        return cloned

    def find_king(self, color: Color) -> tuple[int, int] | None:
        """Encontra a posição do rei de uma determinada cor."""
        for row in range(8):
            for col in range(8):
                piece = self.get_piece(row, col)

                if isinstance(piece, King) and piece.color is color:
                    return (row, col)

        return None

    def is_in_check(self, color: Color) -> bool:
        """Verifica se o rei de uma determinada cor esta atualmente em xeque."""
        king_pos = self.find_king(color)
        if king_pos is None:
            return False
        return self.is_square_attacked(king_pos, color.opposite())

    def has_legal_moves(self, color: Color) -> bool:
        """Verifica se o jogador de uma determinada cor possui ao menos um movimento legal."""
        for r in range(8):
            for c in range(8):
                piece = self.get_piece(r, c)
                if piece is not None and piece.color is color:
                    moves = self.generate_moves_for_piece(r, c)
                    if moves:  # Encontrou pelo menos 1 movimento legal valido
                        return True
        return False

    def is_checkmate(self, color: Color) -> bool:
        """Verifica se o jogador de uma determinada cor esta em xeque-mate."""
        return self.is_in_check(color) and not self.has_legal_moves(color)

    def is_stalemate(self, color: Color) -> bool:
        """Verifica se o jogador de uma determinada cor esta afogado (empate por falta de lances)."""
        return not self.is_in_check(color) and not self.has_legal_moves(color)

    def would_leave_king_in_check(self, move: Move) -> bool:
        """Verifica se uma jogada deixaria o próprio rei em xeque."""
        piece = self.get_piece(*move.start_pos)

        if piece is None:
            return True

        test_board = self.copy()

        test_move = Move(
            start_pos=move.start_pos,
            end_pos=move.end_pos,
            is_castling=move.is_castling,
            is_en_passant=move.is_en_passant,
            requires_promotion=move.requires_promotion,
            promotion_piece=move.promotion_piece,
        )

        if test_move.requires_promotion and test_move.promotion_piece is None:
            test_move.promotion_piece = "Q"

        test_board.execute_move(test_move)

        king_pos = test_board.find_king(piece.color)

        if king_pos is None:
            return False

        return test_board.is_square_attacked(
            king_pos,
            piece.color.opposite()
        )

    def setup_initial_position(self) -> None:
        """Configura o tabuleiro com a disposicao inicial das pecas.

        Parametros:
            Nenhum.
        Retorno:
            None.
        """
        self.grid = [[None for _ in range(8)] for _ in range(8)]

        for col in range(8):
            self.grid[1][col] = Pawn(Color.BLACK)
            self.grid[6][col] = Pawn(Color.WHITE)

        self.grid[0][0] = Rook(Color.BLACK)
        self.grid[0][7] = Rook(Color.BLACK)
        self.grid[7][0] = Rook(Color.WHITE)
        self.grid[7][7] = Rook(Color.WHITE)

        self.grid[0][1] = Knight(Color.BLACK)
        self.grid[0][6] = Knight(Color.BLACK)
        self.grid[7][1] = Knight(Color.WHITE)
        self.grid[7][6] = Knight(Color.WHITE)

        self.grid[0][2] = Bishop(Color.BLACK)
        self.grid[0][5] = Bishop(Color.BLACK)
        self.grid[7][2] = Bishop(Color.WHITE)
        self.grid[7][5] = Bishop(Color.WHITE)

        self.grid[0][3] = Queen(Color.BLACK)
        self.grid[7][3] = Queen(Color.WHITE)

        self.grid[0][4] = King(Color.BLACK)
        self.grid[7][4] = King(Color.WHITE)
        self.en_passant_target = None

    @staticmethod
    def in_bounds(row: int, col: int) -> bool:
        """Verifica se uma coordenada esta dentro dos limites do tabuleiro.

        Parametros:
            row (int): Linha a validar.
            col (int): Coluna a validar.
        Retorno:
            bool: ``True`` quando a coordenada e valida, senao ``False``.
        """
        return 0 <= row < 8 and 0 <= col < 8

    def get_piece(self, row: int, col: int) -> Piece | None:
        """Retorna a peca em uma coordenada do tabuleiro.

        Parametros:
            row (int): Linha da coordenada.
            col (int): Coluna da coordenada.
        Retorno:
            Piece | None: Peca encontrada ou ``None`` se vazio/invalido.
        """
        if not self.in_bounds(row, col):
            return None
        return self.grid[row][col]

    def set_piece(self, row: int, col: int, piece: Piece | None) -> None:
        """Define uma peca em uma coordenada do tabuleiro.

        Parametros:
            row (int): Linha de destino.
            col (int): Coluna de destino.
            piece (Piece | None): Peca a ser posicionada, ou ``None`` para limpar.
        Retorno:
            None.
        """
        if self.in_bounds(row, col):
            self.grid[row][col] = piece

    def is_empty(self, row: int, col: int) -> bool:
        """Informa se uma casa do tabuleiro esta vazia.

        Parametros:
            row (int): Linha da casa.
            col (int): Coluna da casa.
        Retorno:
            bool: ``True`` se nao houver peca na casa.
        """
        return self.get_piece(row, col) is None

    def is_enemy(self, row: int, col: int, color: Color) -> bool:
        """Verifica se a casa contem uma peca inimiga da cor informada.

        Parametros:
            row (int): Linha da casa.
            col (int): Coluna da casa.
            color (Color): Cor de referencia para comparacao.
        Retorno:
            bool: ``True`` quando ha peca inimiga na casa.
        """
        p = self.get_piece(row, col)
        return p is not None and p.color is not color

    def generate_moves_for_piece(self, row: int, col: int) -> list[Move]:
        """Gera movimentos legais para a peca em uma coordenada."""
        piece = self.get_piece(row, col)

        if piece is None:
            return []

        candidate_moves = piece.generate_moves(self, row, col)

        return [
            move
            for move in candidate_moves
            if not self.would_leave_king_in_check(move)
        ]

    def castling_moves_for_king(self, row: int, col: int, king: King) -> list[Move]:
        """Calcula movimentos de roque validos para um rei.

        Parametros:
            row (int): Linha atual do rei.
            col (int): Coluna atual do rei.
            king (King): Rei para o qual os roques serao avaliados.
        Retorno:
            list[Move]: Lista de movimentos de roque legalmente disponiveis.
        """
        home_row = 7 if king.color is Color.WHITE else 0
        if row != home_row or col != 4 or king.has_moved:
            return []

        opponent = king.color.opposite()
        if self.is_square_attacked((row, col), opponent):
            return []

        result: list[Move] = []

        rook_k = self.get_piece(row, 7)
        if isinstance(rook_k, Rook) and rook_k.color is king.color and not rook_k.has_moved:
            if self.is_empty(row, 5) and self.is_empty(row, 6):
                if not self.is_square_attacked((row, 5), opponent) and not self.is_square_attacked((row, 6), opponent):
                    result.append(Move(start_pos=(row, 4), end_pos=(row, 6), is_castling=True))

        rook_q = self.get_piece(row, 0)
        if isinstance(rook_q, Rook) and rook_q.color is king.color and not rook_q.has_moved:
            if self.is_empty(row, 1) and self.is_empty(row, 2) and self.is_empty(row, 3):
                if not self.is_square_attacked((row, 3), opponent) and not self.is_square_attacked((row, 2), opponent):
                    result.append(Move(start_pos=(row, 4), end_pos=(row, 2), is_castling=True))

        return result

    def execute_move(self, move: Move) -> None:
        """Executa um movimento no tabuleiro, incluindo regras especiais.

        Parametros:
            move (Move): Movimento a ser aplicado.
        Retorno:
            None.
        """
        sr, sc = move.start_pos
        er, ec = move.end_pos
        piece = self.get_piece(sr, sc)
        if piece is None:
            raise ValueError("Nao existe peca na origem.")

        if move.requires_promotion and move.promotion_piece is None:
            raise ValueError("Promocao obrigatoria sem escolha de peca.")

        self.en_passant_target = None

        if move.is_en_passant:
            capture_row = er + 1 if piece.color is Color.WHITE else er - 1
            self.set_piece(capture_row, ec, None)

        self.set_piece(sr, sc, None)
        self.set_piece(er, ec, piece)

        if move.is_castling and isinstance(piece, King):
            if ec == 6:
                rook = self.get_piece(er, 7)
                self.set_piece(er, 7, None)
                self.set_piece(er, 5, rook)
                if rook:
                    rook.has_moved = True
            elif ec == 2:
                rook = self.get_piece(er, 0)
                self.set_piece(er, 0, None)
                self.set_piece(er, 3, rook)
                if rook:
                    rook.has_moved = True

        if isinstance(piece, Pawn) and abs(er - sr) == 2:
            self.en_passant_target = ((sr + er) // 2, sc)

        if move.requires_promotion:
            promoted = self._promote_piece(piece.color, move.promotion_piece)
            promoted.has_moved = True
            self.set_piece(er, ec, promoted)

        piece.has_moved = True

    @staticmethod
    def _promote_piece(color: Color, code: str | None) -> Piece:
        """Cria a peca resultante de uma promocao de peao.

        Parametros:
            color (Color): Cor da peca promovida.
            code (str | None): Codigo da peca alvo (Q, R, B, N).
        Retorno:
            Piece: Nova instancia da peca promovida.
        """
        by_code = {
            "Q": Queen,
            "R": Rook,
            "B": Bishop,
            "N": Knight,
        }
        cls = by_code.get((code or "Q").upper())
        if cls is None:
            raise ValueError("Peca de promocao invalida.")
        return cls(color)

    def is_square_attacked(self, pos: tuple[int, int], by_color: Color) -> bool:
        """Determina se uma casa esta sob ataque por pecas de uma cor.

        Parametros:
            pos (tuple[int, int]): Coordenada da casa avaliada.
            by_color (Color): Cor atacante considerada na analise.
        Retorno:
            bool: ``True`` se a casa puder ser capturada por ``by_color``.
        """
        r, c = pos

        pawn_dir = -1 if by_color is Color.WHITE else 1
        for dc in (-1, 1):
            pr, pc = r - pawn_dir, c + dc
            p = self.get_piece(pr, pc)
            if isinstance(p, Pawn) and p.color is by_color:
                return True

        for dr, dc in [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]:
            p = self.get_piece(r + dr, c + dc)
            if isinstance(p, Knight) and p.color is by_color:
                return True

        for dr, dc in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
            nr, nc = r + dr, c + dc
            while self.in_bounds(nr, nc):
                p = self.get_piece(nr, nc)
                if p is not None:
                    if p.color is by_color and (isinstance(p, Bishop) or isinstance(p, Queen)):
                        return True
                    break
                nr += dr
                nc += dc

        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            while self.in_bounds(nr, nc):
                p = self.get_piece(nr, nc)
                if p is not None:
                    if p.color is by_color and (isinstance(p, Rook) or isinstance(p, Queen)):
                        return True
                    break
                nr += dr
                nc += dc

        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if dr == 0 and dc == 0:
                    continue
                p = self.get_piece(r + dr, c + dc)
                if isinstance(p, King) and p.color is by_color:
                    return True

        return False
