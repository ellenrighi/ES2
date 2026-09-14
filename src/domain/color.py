from enum import Enum


class Color(str, Enum):
    """Representa as cores possiveis das pecas no jogo.

    Parametros:
        Nenhum.
    Retorno:
        Instancia de ``Color`` com valor ``WHITE`` ou ``BLACK``.
    """

    WHITE = "WHITE"
    BLACK = "BLACK"

    def opposite(self) -> "Color":
        """Retorna a cor oposta da instancia atual.

        Parametros:
            Nenhum.
        Retorno:
            Color: Cor oposta a atual.
        """
        return Color.BLACK if self is Color.WHITE else Color.WHITE
