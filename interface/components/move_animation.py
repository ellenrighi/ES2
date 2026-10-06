class MoveAnimation:
    """Estado visual de uma jogada, independente do tabuleiro atualizado."""

    DURATION_MS = 350

    def __init__(self):
        self.board = None
        self.move = None
        self.elapsed_ms = 0

    @property
    def active(self):
        return self.move is not None

    def start(self, board, move):
        self.board = board
        self.move = move
        self.elapsed_ms = 0

    def advance(self, delta_ms):
        self.elapsed_ms += delta_ms
        if self.elapsed_ms >= self.DURATION_MS:
            self.move = None
            self.board = None

    def moving_pieces(self):
        moves = [(self.move.start_pos, self.move.end_pos)]
        if self.move.is_castling:
            row, column = self.move.end_pos
            moves.append(((row, 7 if column == 6 else 0),
                          (row, 5 if column == 6 else 3)))
        return moves
