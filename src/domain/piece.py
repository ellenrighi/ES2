from dataclasses import dataclass
from typing import TYPE_CHECKING

from .color import Color
from .move import Move

if TYPE_CHECKING:
    from .board import Board


@dataclass
class Piece:
    """Classe base para todas as pecas de xadrez.

    Parametros:
        color (Color): Cor da peca.
        has_moved (bool): Indica se a peca ja se moveu.
        kind (str): Codigo textual da peca.
    Retorno:
        Instancia de ``Piece`` ou de uma subclasse.
    """

    color: Color
    has_moved: bool = False
    kind: str = "?"

    def copy(self) -> "Piece":
        """Cria uma copia da peca preservando estado relevante.

        Parametros:
            Nenhum.
        Retorno:
            Piece: Nova instancia do mesmo tipo e com o mesmo estado de movimento.
        """
        cloned = type(self)(self.color)
        cloned.has_moved = self.has_moved
        return cloned

    def generate_moves(self, board: "Board", row: int, col: int) -> list[Move]:
        """Gera movimentos legais da peca na posicao informada.

        Parametros:
            board (Board): Tabuleiro atual da partida.
            row (int): Linha de origem da peca.
            col (int): Coluna de origem da peca.
        Retorno:
            list[Move]: Lista de movimentos possiveis para a peca.
        """
        return []

    @staticmethod
    def _sliding_moves(
        board: "Board",
        row: int,
        col: int,
        color: Color,
        directions: list[tuple[int, int]],
    ) -> list[Move]:
        """Calcula movimentos de pecas deslizantes em direcoes lineares.

        Parametros:
            board (Board): Tabuleiro atual da partida.
            row (int): Linha de origem.
            col (int): Coluna de origem.
            color (Color): Cor da peca que esta movendo.
            directions (list[tuple[int, int]]): Vetores de direcao (delta_linha, delta_coluna).
        Retorno:
            list[Move]: Lista de movimentos validos nas direcoes informadas.
        """
        moves: list[Move] = []
        for dr, dc in directions:
            nr, nc = row + dr, col + dc
            while board.in_bounds(nr, nc):
                dst = board.get_piece(nr, nc)
                if dst is None:
                    moves.append(Move(start_pos=(row, col), end_pos=(nr, nc)))
                else:
                    if dst.color is not color:
                        moves.append(Move(start_pos=(row, col), end_pos=(nr, nc)))
                    break
                nr += dr
                nc += dc
        return moves


class Pawn(Piece):
    """Representa um peao e suas regras de movimentacao.

    Parametros:
        color (Color): Cor do peao.
        has_moved (bool): Indica se o peao ja se moveu.
        kind (str): Codigo textual da peca.
    Retorno:
        Instancia de ``Pawn``.
    """

    kind = "P"

    def generate_moves(self, board: "Board", row: int, col: int) -> list[Move]:
        """Gera movimentos validos do peao, incluindo captura e promocao.

        Parametros:
            board (Board): Tabuleiro atual da partida.
            row (int): Linha atual do peao.
            col (int): Coluna atual do peao.
        Retorno:
            list[Move]: Movimentos legais do peao para o turno atual.
        """
        moves: list[Move] = []
        direction = -1 if self.color is Color.WHITE else 1
        start_row = 6 if self.color is Color.WHITE else 1
        promotion_row = 0 if self.color is Color.WHITE else 7

        one_step = row + direction
        if board.in_bounds(one_step, col) and board.is_empty(one_step, col):
            moves.append(
                Move(
                    start_pos=(row, col),
                    end_pos=(one_step, col),
                    requires_promotion=one_step == promotion_row,
                )
            )
            two_step = row + (2 * direction)
            if row == start_row and board.in_bounds(two_step, col) and board.is_empty(two_step, col):
                moves.append(Move(start_pos=(row, col), end_pos=(two_step, col)))

        for dc in (-1, 1):
            nr, nc = row + direction, col + dc
            if not board.in_bounds(nr, nc):
                continue
            if board.is_enemy(nr, nc, self.color):
                moves.append(
                    Move(
                        start_pos=(row, col),
                        end_pos=(nr, nc),
                        requires_promotion=nr == promotion_row,
                    )
                )

        if board.en_passant_target is not None:
            target_row, target_col = board.en_passant_target
            if target_row == row + direction and abs(target_col - col) == 1:
                moves.append(
                    Move(
                        start_pos=(row, col),
                        end_pos=(target_row, target_col),
                        is_en_passant=True,
                    )
                )

        return moves


class Knight(Piece):
    """Representa um cavalo e seu movimento em L.

    Parametros:
        color (Color): Cor do cavalo.
        has_moved (bool): Indica se o cavalo ja se moveu.
        kind (str): Codigo textual da peca.
    Retorno:
        Instancia de ``Knight``.
    """

    kind = "N"

    def generate_moves(self, board: "Board", row: int, col: int) -> list[Move]:
        """Gera movimentos validos do cavalo a partir da posicao atual.

        Parametros:
            board (Board): Tabuleiro atual da partida.
            row (int): Linha atual do cavalo.
            col (int): Coluna atual do cavalo.
        Retorno:
            list[Move]: Movimentos legais do cavalo.
        """
        moves: list[Move] = []
        jumps = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]
        for dr, dc in jumps:
            nr, nc = row + dr, col + dc
            if not board.in_bounds(nr, nc):
                continue
            dst = board.get_piece(nr, nc)
            if dst is None or dst.color is not self.color:
                moves.append(Move(start_pos=(row, col), end_pos=(nr, nc)))
        return moves


class Bishop(Piece):
    """Representa um bispo e seu movimento nas diagonais.

    Parametros:
        color (Color): Cor do bispo.
        has_moved (bool): Indica se o bispo ja se moveu.
        kind (str): Codigo textual da peca.
    Retorno:
        Instancia de ``Bishop``.
    """

    kind = "B"

    def generate_moves(self, board: "Board", row: int, col: int) -> list[Move]:
        """Gera movimentos diagonais validos do bispo.

        Parametros:
            board (Board): Tabuleiro atual da partida.
            row (int): Linha atual do bispo.
            col (int): Coluna atual do bispo.
        Retorno:
            list[Move]: Movimentos legais do bispo.
        """
        return self._sliding_moves(board, row, col, self.color, [(-1, -1), (-1, 1), (1, -1), (1, 1)])


class Rook(Piece):
    """Representa uma torre e seu movimento em linhas retas.

    Parametros:
        color (Color): Cor da torre.
        has_moved (bool): Indica se a torre ja se moveu.
        kind (str): Codigo textual da peca.
    Retorno:
        Instancia de ``Rook``.
    """

    kind = "R"

    def generate_moves(self, board: "Board", row: int, col: int) -> list[Move]:
        """Gera movimentos ortogonais validos da torre.

        Parametros:
            board (Board): Tabuleiro atual da partida.
            row (int): Linha atual da torre.
            col (int): Coluna atual da torre.
        Retorno:
            list[Move]: Movimentos legais da torre.
        """
        return self._sliding_moves(board, row, col, self.color, [(-1, 0), (1, 0), (0, -1), (0, 1)])


class Queen(Piece):
    """Representa a dama e seu movimento combinado de torre e bispo.

    Parametros:
        color (Color): Cor da dama.
        has_moved (bool): Indica se a dama ja se moveu.
        kind (str): Codigo textual da peca.
    Retorno:
        Instancia de ``Queen``.
    """

    kind = "Q"

    def generate_moves(self, board: "Board", row: int, col: int) -> list[Move]:
        """Gera movimentos diagonais e ortogonais validos da dama.

        Parametros:
            board (Board): Tabuleiro atual da partida.
            row (int): Linha atual da dama.
            col (int): Coluna atual da dama.
        Retorno:
            list[Move]: Movimentos legais da dama.
        """
        return self._sliding_moves(
            board,
            row,
            col,
            self.color,
            [(-1, -1), (-1, 1), (1, -1), (1, 1), (-1, 0), (1, 0), (0, -1), (0, 1)],
        )


class King(Piece):
    """Representa o rei e seus movimentos de uma casa, incluindo roque.

    Parametros:
        color (Color): Cor do rei.
        has_moved (bool): Indica se o rei ja se moveu.
        kind (str): Codigo textual da peca.
    Retorno:
        Instancia de ``King``.
    """

    kind = "K"

    def generate_moves(self, board: "Board", row: int, col: int) -> list[Move]:
        """Gera movimentos validos do rei e adiciona movimentos de roque.

        Parametros:
            board (Board): Tabuleiro atual da partida.
            row (int): Linha atual do rei.
            col (int): Coluna atual do rei.
        Retorno:
            list[Move]: Movimentos legais do rei.
        """
        moves: list[Move] = []
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if dr == 0 and dc == 0:
                    continue
                nr, nc = row + dr, col + dc
                if not board.in_bounds(nr, nc):
                    continue
                dst = board.get_piece(nr, nc)
                if dst is None or dst.color is not self.color:
                    moves.append(Move(start_pos=(row, col), end_pos=(nr, nc)))

        moves.extend(board.castling_moves_for_king(row, col, self))
        return moves
