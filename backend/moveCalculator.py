from .board import Board
from .piece import Piece
from .util import to_python_indecies, X_LINE


class Dir:
    Up = 0
    Down = 1
    Right = 2
    Left = 3

class Diag:
    UpRight     = (Dir.Up,      Dir.Right)
    DownRight   = (Dir.Down,    Dir.Right)
    UpLeft      = (Dir.Up,      Dir.Left)
    DownLeft    = (Dir.Down,    Dir.Left)

def validMoves(board: Board, square: str) -> list:
    piece = board.get_piece(square)
    x, y = to_python_indecies(square)
    return piece_function[piece.name](board, x, y, piece)
    
def _pawn(board: Board, x: int, y: int, piece: Piece) -> None:
    forward = get_forward_for_piece(piece)
    possible_moves = list()
    
    can_go(x, y, forward, piece, possible_moves, board)
        
    if is_pawn_home(y, piece):
        new_x, new_y = move(x, y, forward)
        can_go(new_x, new_y, forward, piece, possible_moves, board)
        
    can_take(x,y, (forward, Dir.Right), piece, possible_moves, board)
    can_take(x,y, (forward, Dir.Left), piece, possible_moves, board)

    return possible_moves
    
def can_take(x: int, y: int, dir: Dir | tuple, piece: Piece, possible_moves: list, board: Board) -> bool:
    new_x, new_y = move(x,y, dir)
    if not in_boundaries(new_x, new_y):
        return False
    can_take = board.has_piece((new_x, new_y)) and are_hostile(piece, board.get_piece((new_x, new_y)))
    if can_take:
        possible_moves.append((new_x, new_y))
    return can_take
        
def can_go(x: int, y: int, dir: Dir | tuple, piece: Piece, possible_moves: list, board: Board) -> bool:
    new_x, new_y = move(x,y,dir)
    can_go = in_boundaries(new_x, new_y) and not board.has_piece((new_x, new_y))
    if can_go:
        possible_moves.append((new_x, new_y))
    return can_go
    
def _rook(board: Board, x: int, y: int, piece: Piece) -> None:
    possible_moves = list()
    if not can_take(x,y, Dir.Up, piece, possible_moves, board):
        if not can_go(x,y,Dir.Up, piece, possible_moves, board):
            pass
        

def _bishop(board: Board, x: int, y: int, piece: Piece) -> None:
    pass    
def _knight(board: Board, x: int, y: int, piece: Piece) -> None:
    pass    
def _king(board: Board, x: int, y: int, piece: Piece) -> None:
    pass    
def _queen(board: Board, x: int, y: int, piece: Piece) -> None:
    pass    

def move(x: int, y: int, dir: int | tuple) -> str:
    if isinstance(dir, int):
        if dir == Dir.Up:
            return x, y+1
        elif dir == Dir.Down:
            return x, y-1
        elif dir == Dir.Right:
            return x+1, y
        elif dir == Dir.Left:
            return x-1, y
    if isinstance(dir, tuple):
        for d in dir:
            x, y = move(x,y,d)
        return x,y
    
def in_boundaries(value_1: int, value_2: int = None) -> bool:
    if value_2 is None:
        return 0 <= value_1 and 9 > value_1
    else:
        return 0 <= value_1 and 9 > value_1 and 0 <= value_2 and 9 > value_2
    
def are_hostile(piece_1: Piece, piece_2: Piece) -> bool:
    return piece_1.color != piece_2.color

def get_forward_for_piece(piece: Piece) -> Dir:
    if piece.color == Piece.Color.White:
        return Dir.Up
    elif piece.color == Piece.Color.Black:
        return Dir.Down
    
def is_pawn_home(y: int, piece: Piece) -> bool:
    if piece.name != Piece.Figure.Pawn:
        raise Exception("You checked if pawn is home, but piece is not a pawn")
    return piece.color == Piece.Color.White and y == 1 or piece.color == Piece.Color.Black and y == 6

piece_function = {
    Piece.Figure.Pawn : _pawn,
    Piece.Figure.Rook : _rook,
    Piece.Figure.Bishop: _bishop,
    Piece.Figure.Knight: _knight,
    Piece.Figure.King : _king,
    Piece.Figure.Queen : _queen    
}