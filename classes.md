@startuml
skinparam classAttributeIconSize 0
skinparam monochrome false
skinparam roundcorner 8
skinparam linetype ortho

enum Color {
  WHITE
  BLACK
}

enum GameStatus {
  ONGOING
  CHECK
  CHECKMATE
  STALEMATE
  DRAW
}

class Move {
  +Tuple start_pos
  +Tuple end_pos
  +Piece piece_moved
  +Piece piece_captured
  +bool is_castling
  +bool is_en_passant
  +String promotion_piece
}

abstract class Piece {
  #Color color
  #Tuple position
  #bool has_moved
  +{abstract} get_pseudo_legal_moves(board: Board): List<Move>
}

class Pawn {
  +get_pseudo_legal_moves(board: Board): List<Move>
}
class Knight {
  +get_pseudo_legal_moves(board: Board): List<Move>
}
class Bishop {
  +get_pseudo_legal_moves(board: Board): List<Move>
}
class Rook {
  +get_pseudo_legal_moves(board: Board): List<Move>
}
class Queen {
  +get_pseudo_legal_moves(board: Board): List<Move>
}
class King {
  +get_pseudo_legal_moves(board: Board): List<Move>
}

class Board {
  -Piece[8][8] grid
  -Tuple en_passant_target
  -int halfmove_clock
  +get_piece(row: int, col: int): Piece
  +set_piece(row: int, col: int, piece: Piece): void
  +execute_move(move: Move): void
  +is_square_attacked(pos: Tuple, by_color: Color): bool
  +clone(): Board
}

class RuleValidator {
  +is_in_check(board: Board, color: Color): bool
  +is_checkmate(board: Board, color: Color): bool
  +is_stalemate(board: Board, color: Color): bool
  +is_insufficient_material(board: Board): bool
  +is_fifty_move_rule(halfmove_clock: int): bool
  +is_threefold_repetition(history: List<Board>): bool
}

class AIPlayer {
  -int depth
  +choose_move(board: Board): Move
  -evaluate_board(board: Board): int
  -minimax(board: Board, depth: int, alpha: int, beta: int, is_max: bool): int
}

class Game {
  -Board board
  -Color current_turn
  -GameStatus status
  -List<Move> move_history
  +make_move(move: Move): bool
  +get_legal_moves(): List<Move>
  +is_game_over(): bool
  +restart_game(): void
}

class ChessGUI {
  -Game game
  -Tuple selected_square
  +run(): void
  +handle_click(x: int, y: int): void
  +draw_board(): void
  +draw_pieces(): void
  +show_game_over_screen(): void
}

' Herança
Piece <|-- Pawn
Piece <|-- Knight
Piece <|-- Bishop
Piece <|-- Rook
Piece <|-- Queen
Piece <|-- King

' Relacionamentos
ChessGUI --> Game : interage
Game *-- Board : possui
Game --> RuleValidator : valida regras
Game --> AIPlayer : solicita jogada
Game o-- Move : histórico
Board *-- Piece : contém (8x8)
Piece --> Color : possui
Game --> GameStatus : gerencia

@enduml