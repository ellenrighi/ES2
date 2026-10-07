from dataclasses import dataclass
from typing import Optional


@dataclass
class Move:
    """Representa um movimento de uma peca no tabuleiro.

    Parametros:
        start_pos (tuple[int, int]): Coordenada de origem no formato (linha, coluna).
        end_pos (tuple[int, int]): Coordenada de destino no formato (linha, coluna).
        is_castling (bool): Indica se o movimento e um roque.
        is_en_passant (bool): Indica se o movimento e uma captura en passant.
        requires_promotion (bool): Indica se o movimento exige promocao de peao.
        promotion_piece (Optional[str]): Codigo da peca de promocao (Q, R, B ou N).
    Retorno:
        Instancia de ``Move``.
    """

    start_pos: tuple[int, int]
    end_pos: tuple[int, int]
    is_castling: bool = False
    is_en_passant: bool = False
    requires_promotion: bool = False
    promotion_piece: Optional[str] = None
