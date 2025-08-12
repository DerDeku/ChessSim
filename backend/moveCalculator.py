from enum import Enum

from .board import Board
from .piece import Piece
from .util import to_python_indecies, X_LINE

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
        self.color_to_move = None
        self.board = board
        self.piece_function = {
        Piece.Figure.Pawn : self._pawn,
        Piece.Figure.Rook : self._rook,
        Piece.Figure.Bishop : self._bishop,
        Piece.Figure.Knight : self._knight,
        Piece.Figure.King : self._king,
        Piece.Figure.Queen : self._queen
        }
    
    def validMoves(self, square: str | None = None, piece: Piece | None = None) -> list:
        if square and not piece:
            piece = self.board.get_piece(square)
        self.color_to_move = piece.color
        return self.piece_function[piece.name](piece)

    def _pawn(self, piece: Piece) -> None:
        self.possible_moves = list()
        forward = self._get_forward_for_piece(piece)
        self._can_go(piece.pos, forward, piece)

        if self._is_pawn_home(piece):
            new_pos = self._move(piece.pos, forward)
            self._can_go(new_pos, forward, piece)

        self._can_take((forward, Dir.Right), piece)
        self._can_take((forward, Dir.Left), piece)
        return self.possible_moves

    def _rook(self, piece: Piece) -> None:
        self.possible_moves = list()
        for dir in Dir.Dirs:
            self._find_end(piece.pos, piece, dir)
        return self.possible_moves

    def _bishop(self, piece: Piece) -> None:
        self.possible_moves = list()
        for diag in Diag.Diags:
            self._find_end(piece.pos, piece, diag)
        return self.possible_moves

    def _knight(self, piece: Piece) -> None:
        self.possible_moves = list()
        for knight_move in Knight_Moves:
            self._knight_move(piece, knight_move)
        return self.possible_moves
    
    def _king(self, piece: Piece) -> None:
        self.possible_moves = list()
        for dir in Dir.Dirs:
            self._king_move(piece, dir)
        for diag in Diag.Diags:
            self._king_move(piece, diag)
        return self.possible_moves 
    
    def _queen(self, piece: Piece) -> None:
        self.possible_moves = list()
        for dir in Dir.Dirs:
            self._find_end(piece.pos, piece, dir)
        for diag in Diag.Diags:
            self._find_end(piece.pos, piece, diag)
        return self.possible_moves
    
    def _king_move(self, piece: Piece, dir: int | tuple) -> None:
            new_pos = self._move(piece.pos, dir)
            enemy_king_pos = self.board.get_enemys_king_position(piece.color)
            if not self._in_boundaries(new_pos):
                return
            if self.board.kings_to_close(new_pos, enemy_king_pos):
                return
            if self.board.has_piece(new_pos):
                if self._are_hostile(piece, self.board.get_piece(new_pos)):
                    self.possible_moves.append(new_pos)
                return
            if self.king_under_attack(new_pos, piece):
                return
            self.possible_moves.append(new_pos)

    def king_under_attack_if_piece_goes(self, new_pos: tuple, piece: Piece) -> bool:
        old_pos = piece.pos
        old_piece = self.board.move_to(old_pos, new_pos)
        check = self.king_under_attack()
        self.board.move_to(new_pos, old_pos)
        if old_piece:
            self.board._get_square(new_pos).place_piece(old_piece)
        return check
            
    def king_under_attack(self, pos: tuple | None = None, piece: Piece | None = None) -> bool:
        if pos is None and piece is None:
            piece = self.board.get_king_from_color(self.color_to_move)
            pos = piece.pos

        if piece.name != Piece.Figure.King:
            raise Exception(f"Piece {piece.name} is not a King as expected")
        
        for dir in Dir.Dirs:
            pieces = [Piece.Figure.Queen, Piece.Figure.Rook]
            new_piece = self.find_piece_in_dir(pos, dir)
            if new_piece and new_piece.color != piece.color and new_piece.name in pieces:
                return True

        for diag in Diag.Diags:
            pieces = [Piece.Figure.Queen, Piece.Figure.Bishop]
            new_piece = self.find_piece_in_dir(pos, diag)
            if new_piece and new_piece.color != piece.color and new_piece.name in pieces:
                return True
        
        for dir in Dir.Dirs:
            pieces = [Piece.Figure.Pawn]
            new_piece = self.find_piece_in_dir(pos, dir, repeat=False)
            if new_piece and new_piece.color != piece.color and new_piece.name in pieces:
                return True
        
        for dirs in Knight_Moves:
            pieces = [Piece.Figure.Knight]
            new_piece = self.find_piece_in_dir(pos, dirs, repeat=False)
            if new_piece and new_piece.color != piece.color and new_piece.name in pieces:
                return True
        return False

    def find_piece_in_dir(self, pos: tuple, dir: Dir | tuple, repeat: bool = True) -> Piece | None:
        while True:
            new_pos = self._move(pos, dir)
            if not self._in_boundaries(new_pos):
                return None
            if not self.board.has_piece(new_pos):
                if repeat:
                    pos = new_pos
                    continue
                else:
                    return None
            piece = self.board.get_piece(new_pos)
            return piece
            
    def _knight_move(self, piece: Piece, dir: tuple):
        if self._can_go(piece.pos, dir, piece):
            return
        if self._can_take(dir, piece):
            return
        
    def _find_end(self, pos: tuple, piece: Piece, dir: int | tuple) -> None:
        repeat = True
        while repeat:
            new_pos = self._move(pos, dir)
            if not self._in_boundaries(new_pos):
                return
            if self.board.has_piece(new_pos):
                repeat = False
                if not self._are_hostile(piece, self.board.get_piece(new_pos)):
                    return
            if not self.king_under_attack_if_piece_goes(new_pos, piece):
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
        can_take = self.board.has_piece(new_pos) and self._are_hostile(piece, self.board.get_piece(new_pos)) and self.king_under_attack_if_piece_goes(new_pos, piece)
        if can_take:
            self.possible_moves.append(new_pos)
        return can_take

    def _can_go(self, pos: tuple, dir: Dir | tuple, piece: Piece) -> bool:
        new_pos = self._move(pos, dir)
        can_go = self._in_boundaries(new_pos) and not self.board.has_piece(new_pos) and not self.king_under_attack_if_piece_goes(new_pos, piece)
        if can_go:
            self.possible_moves.append(new_pos)
        return can_go