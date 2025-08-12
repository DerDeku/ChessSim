from enum import Enum

from ..chess import Board
from ..chess import Piece
from ..chess import util


class Dir:
    Up = 0
    Down = 1
    Right = 2
    Left = 3
    Dirs = [Up, Down, Right, Left]

class Diag:
    UpRight     = (Dir.Up,      Dir.Right)
    DownRight   = (Dir.Down,    Dir.Right)
    UpLeft      = (Dir.Up,      Dir.Left)
    DownLeft    = (Dir.Down,    Dir.Left)
    Diags       = [UpRight, DownRight, UpLeft, DownLeft]
    
Knight_Moves = [(Dir.Up, Diag.UpRight),(Dir.Up, Diag.UpLeft),(Dir.Right, Diag.UpRight),(Dir.Right, Diag.DownRight),(Dir.Down, Diag.DownRight),(Dir.Down, Diag.DownLeft),(Dir.Left, Diag.UpLeft),(Dir.Left, Diag.DownLeft)]

class MoveCalculator:
    def __init__(self, board: Board):
        self.board = board
        self.piece_function = {
        Piece.Figure.Pawn : self._pawn,
        Piece.Figure.Rook : self._rook,
        Piece.Figure.Bishop : self._bishop,
        Piece.Figure.Knight : self._knight,
        Piece.Figure.King : self._king,
        Piece.Figure.Queen : self._queen    
        }
    
    def use_board(self, board: Board) -> None:
        self.board = board
    
    def validMoves(self, square: str | None = None, piece: Piece | None = None) -> list:
        if square and not piece:
            piece = self.board.get_piece(square)
        return self.piece_function[piece.name](piece) if piece else []

    def _pawn(self, piece: Piece) -> None:
        self.possible_moves = list()
        forward = self._get_forward_for_piece(piece)
        self._can_go(piece.pos, forward)

        if self._is_pawn_home(piece):
            new_pos = self._move(piece.pos, forward)
            self._can_go(new_pos, forward)

        self._can_take((forward, Dir.Right), piece)
        self._can_take((forward, Dir.Left), piece)
        return self.possible_moves

    def _rook(self, piece: Piece) -> None:
        self.possible_moves = list()
        self._find_end(piece.pos, piece, Dir.Up)
        self._find_end(piece.pos, piece, Dir.Down)
        self._find_end(piece.pos, piece, Dir.Left)
        self._find_end(piece.pos, piece, Dir.Right)
        return self.possible_moves

    def _bishop(self, piece: Piece) -> None:
        self.possible_moves = list()
        self._find_end(piece.pos, piece, Diag.UpRight)
        self._find_end(piece.pos, piece, Diag.DownRight)
        self._find_end(piece.pos, piece, Diag.DownLeft)
        self._find_end(piece.pos, piece, Diag.UpLeft)
        return self.possible_moves

    def _knight(self, piece: Piece) -> None:
        self.possible_moves = list()
        self._knight_move(piece, (Dir.Up, Diag.UpRight))
        self._knight_move(piece, (Dir.Up, Diag.UpLeft))
        self._knight_move(piece, (Dir.Right, Diag.UpRight))
        self._knight_move(piece, (Dir.Right, Diag.DownRight))
        self._knight_move(piece, (Dir.Down, Diag.DownRight))
        self._knight_move(piece, (Dir.Down, Diag.DownLeft))
        self._knight_move(piece, (Dir.Left, Diag.UpLeft))
        self._knight_move(piece, (Dir.Left, Diag.DownLeft))
        return self.possible_moves
    
    def _king(self, piece: Piece) -> None:
        self.possible_moves = list()
        self._king_move(piece, Dir.Up)
        self._king_move(piece, Dir.Down)
        self._king_move(piece, Dir.Left)
        self._king_move(piece, Dir.Right)
        self._king_move(piece, Diag.UpRight)
        self._king_move(piece, Diag.DownRight)
        self._king_move(piece, Diag.DownLeft)
        self._king_move(piece, Diag.UpLeft)
        return self.possible_moves 
    
    def _queen(self, piece: Piece) -> None:
        self.possible_moves = list()
        self._find_end(piece.pos, piece, Dir.Up)
        self._find_end(piece.pos, piece, Dir.Down)
        self._find_end(piece.pos, piece, Dir.Left)
        self._find_end(piece.pos, piece, Dir.Right)
        self._find_end(piece.pos, piece, Diag.UpRight)
        self._find_end(piece.pos, piece, Diag.DownRight)
        self._find_end(piece.pos, piece, Diag.DownLeft)
        self._find_end(piece.pos, piece, Diag.UpLeft)
        return self.possible_moves
    
    def _king_move(self, piece: Piece, dir: int | tuple) -> None:
            new_pos = self._move(piece.pos, dir)
            enemy_king_pos = self.board.get_enemys_king_position(piece.color)
            if self.board.kings_to_close(new_pos, enemy_king_pos):
                return
            if self.king_is_not_safe(new_pos, piece):
                return
            if not self._in_boundaries(new_pos):
                return
            if self.board.has_piece(new_pos):
                if self._are_hostile(piece, self.board.get_piece(new_pos)):
                    self.possible_moves.append(new_pos)
                return
            self.possible_moves.append(new_pos)
            
    def king_is_not_safe(self, pos: tuple, piece: Piece) -> bool:
        if piece.name != Piece.Figure.King:
            raise Exception(f"Piece {piece.name} is not a King as expected")
        
        # TODO: ROOK, BISHOP, QUEEN
        for dir in Dir.Dirs:
            pieces = [Piece.Figure.Queen, Piece.Figure.Rook]
            new_piece = self.find_piece_in_dir(pos, dir)
            if new_piece.color != piece.color and new_piece.name in pieces:
                return True

        for diag in Diag.Diags:
            pieces = [Piece.Figure.Queen, Piece.Figure.Bishop]
            new_piece = self.find_piece_in_dir(pos, diag)
            if new_piece.color != piece.color and new_piece.name in pieces:
                return True
        
        # TODO: PAWN
        # TODO: KNIGHT
        
        for dirs in Knight_Moves:
            pieces = [Piece.Figure.Queen, Piece.Figure.Bishop]
            new_piece = self.find_piece_in_dir(pos, diag)
            if new_piece.color != piece.color and new_piece.name in pieces:
                return True

    def find_piece_in_dir(self, pos: tuple, dir: Dir | tuple, repeat: bool = True) -> Piece | None:
        while True:
            new_pos = self._move(pos, dir)
            if not self._in_boundaries(new_pos):
                return None
            if not self.board.has_piece(new_pos):
                if repeat:
                    continue
                else:
                    return None
            piece = self.board.get_piece(new_pos)
            return piece
            
            

    def _knight_move(self, piece: Piece, dir: tuple):
        if self._can_go(piece.pos, dir):
            return
        if self._can_take(dir, piece):
            return
        
    def _find_end(self, pos: tuple, piece: Piece, dir: int | tuple) -> None:
        while True:
            new_pos = self._move(pos, dir)
            if not self._in_boundaries(new_pos):
                return
            if self.board.has_piece(new_pos):
                if self._are_hostile(piece, self.board.get_piece(new_pos)):
                    self.possible_moves.append(new_pos)
                return
            self.possible_moves.append(new_pos)
            pos = new_pos

    def _move(self, pos: tuple, dir: int | tuple) -> tuple:
        if isinstance(dir, int):
            if dir == Dir.Up:
                return (pos[0], pos[1] + 1)
            elif dir == Dir.Down:
                return (pos[0], pos[1]-1)
            elif dir == Dir.Right:
                return (pos[0]+1, pos[1])
            elif dir == Dir.Left:
                return (pos[0]-1, pos[1])
        if isinstance(dir, tuple):
            for d in dir:
                pos = self._move(pos,d)
            return pos

    def _in_boundaries(self, pos: tuple) -> bool:
        return 0 <= pos[0] < 8 and 0 <= pos[1] < 8

    def _are_hostile(self, piece_1: Piece, piece_2: Piece) -> bool:
        return piece_1.color != piece_2.color

    def _get_forward_for_piece(self, piece: Piece) -> Dir:
        if piece.color == Piece.Color.White:
            return Dir.Up
        elif piece.color == Piece.Color.Black:
            return Dir.Down

    def _is_pawn_home(self, piece: Piece) -> bool:
        y = piece.pos[1]
        if piece.name != Piece.Figure.Pawn:
            raise Exception("You checked if pawn is home, but piece is not a pawn")
        return piece.color == Piece.Color.White and y == 1 or piece.color == Piece.Color.Black and y == 6

    def _can_take(self, dir: Dir | tuple, piece: Piece) -> bool:
        new_pos = self._move(piece.pos, dir)
        if not self._in_boundaries(new_pos):
            return False
        can_take = self.board.has_piece(new_pos) and self._are_hostile(piece, self.board.get_piece(new_pos))
        if can_take:
            self.possible_moves.append(new_pos)
        return can_take

    def _can_go(self, pos: tuple, dir: Dir | tuple) -> bool:
        new_pos = self._move(pos, dir)
        can_go = self._in_boundaries(new_pos) and not self.board.has_piece(new_pos)
        if can_go:
            self.possible_moves.append(new_pos)
        return can_go