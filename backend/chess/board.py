from . import Square
from . import Piece
from . import util

from copy import deepcopy
import os

DIMENSION = 8

class Board:
    def __init__(self):
        self.squares: list[list[Square]] = list()
        self.kings: list[Piece] = list()
        self.pieces: dict[str, list[Piece]] = dict()
        self.en_passant: tuple | None = None
    
    def get_copy(self) -> "Board":
        copy = Board()
        copy.squares = self.squares.copy()
        copy.kings = self.kings.copy()
        copy.pieces = deepcopy(self.pieces.copy())
        return copy
        
    def as_fen(self) -> str:
        pass # TODO return board in FEN format: "rnbqkbnr/pppppppp/8/8/8/8/pppppppp/rnbqkbnr"
    
    def setup_board(self) -> None:
        self._create_board()
        self._create_pieces()
        self._place_pieces()
        print()
        
    def cls(self) -> None:
        os.system("cls")
        
    def show_board(self, highlights: list[tuple] | None = None, highlight_square_name: str | None = None) -> None:
        self.cls()
        print("\n")
        if highlight_square_name:
            highlight_square = util.to_python_indecies(highlight_square_name)
        for y, y_line in enumerate(reversed(self.squares)):
            y = len(self.squares) - y
            print_line = f"{y}    "
            for x, square in enumerate(y_line):
                if highlights and (x,y-1) in highlights:
                    print_line += self.color_line(square.content, "[31m") #red
                elif highlight_square_name and highlight_square == (x,y-1):
                    print_line += self.color_line(square.content,  "[32m") # green 
                else:
                    print_line += f" {square.content} "
            print(print_line)
        print("\n      A  B  C  D  E  F  G  H\n")
        
    def color_line(self, line: str, color: str) -> str:
        prefix = "\033"
        suffix = "\033[0m"
        
        return f" {prefix}{color}{line}{suffix} "
    
    def move_to(self, start_square_pos: str | tuple, target_square_pos: str | tuple, check_en_passant: bool = True) -> None | Piece:
        start_square = self._get_square(start_square_pos)
        piece = start_square.remove_piece()
        target_square = self._get_square(target_square_pos)
        taken_piece = target_square.place_piece(piece)
        if check_en_passant:
            self.handle_en_passant(piece, start_square, target_square)
        return taken_piece
        
    def handle_en_passant(self, piece: Piece, start_square: Square, target_square: Square) -> None:
        # move_to always calls this function currently, also when checking for check multiple times.
        # TODO: fix this
        if piece.name != Piece.Figure.Pawn:
            return
        
        pos_1 = start_square.pos()
        pos_2 = target_square.pos()
        if pos_2 == self.en_passant:
            self.en_passant = None  
            pos_2 = (pos_2[0],pos_2[1]-1) if pos_2[1] == 3 else (pos_2[0], pos_2[1]+1)
            self.remove_piece_from_game(self.get_piece(pos_2))
            
        elif abs(pos_1[1] - pos_2[1]) > 1:
            self.en_passant = (piece.pos[0], piece.pos[1]-1) if piece.color == Piece.Color.White else (piece.pos[0], piece.pos[1]+1)
        else:
            self.en_passant = None
    
    def remove_piece_from_game(self, piece: Piece) -> None:
        self.pieces[piece.color].remove(piece)
        self._get_square(piece.pos).remove_piece()
    
    def get_piece(self, square: str | tuple) -> Piece:
        if isinstance(square, str):
            x, y = util.to_python_indecies(square)
        else:
            x,y = square
        if self.has_piece((x,y)):
            return self.squares[y][x].content
        else:
            raise Exception(f"No piece on square {square}")
        
    def can_pawn_promote(self, piece: Piece) -> bool:
        return piece.color == Piece.Color.White and piece.pos[1] == 7 or piece.color == Piece.Color.Black and piece.pos[1] == 0
        
    def kings_to_close(self, pos_k1: tuple, pos_k2: tuple) -> bool:
        return abs(pos_k1[0]-pos_k2[0]) < 2 and abs(pos_k1[1]-pos_k2[1]) < 2
        
    def get_enemys_king_position(self, own_color: str) -> tuple:
        return self.kings[1].pos if own_color == util.PlayerColor.White else self.kings[0].pos
    
    def get_king_from_color(self, color: str) -> Piece:
        return self.kings[0] if color == util.PlayerColor.White else self.kings[1] 
    
    def _get_square(self, square: str | tuple) -> Square:
        if isinstance(square, str):
            x, y = util.to_python_indecies(square)
        elif isinstance(square, tuple):
            x, y = square
        return self.squares[y][x]

    def has_piece(self, square: str | tuple[int, int]) -> bool:
        if isinstance(square, str):
            x, y = util.to_python_indecies(square)
        elif isinstance(square, tuple):
            x, y = square
        return isinstance(self.squares[y][x].content, Piece)

    def _create_board(self) -> None:    
        for y in range(DIMENSION):
            self.squares.append(list())
            for x in range(DIMENSION):
                square = Square()
                square.set_pos(x,y)
                self.squares[y].append(square)        
                
    def _create_pieces(self) -> list:
        self.pieces: dict[str, list[Piece]] = dict()
        for color in [Piece.Color.White, Piece.Color.Black]:
            pieces_list = list()
            self.pieces.setdefault(color, pieces_list)
            pieces_list.append(Piece(Piece.Figure.Rook, color))
            pieces_list.append(Piece(Piece.Figure.Knight, color))
            pieces_list.append(Piece(Piece.Figure.Bishop, color))
            pieces_list.append(Piece(Piece.Figure.Queen, color))
            pieces_list.append(Piece(Piece.Figure.King, color))
            self.kings.append(pieces_list[-1])
            pieces_list.append(Piece(Piece.Figure.Bishop, color))
            pieces_list.append(Piece(Piece.Figure.Knight, color))
            pieces_list.append(Piece(Piece.Figure.Rook, color))
            for _ in range(8):
                pieces_list.append(Piece(Piece.Figure.Pawn, color))
                
    def _place_pieces(self) -> None:        
        for x, piece in enumerate(self.pieces[util.PlayerColor.White][0:8]):
            self.squares[0][x].place_piece(piece)
            piece.set_pos((x, 0))
        for x, white_pawn in enumerate(self.pieces[util.PlayerColor.White][8:16]):
            self.squares[1][x].place_piece(white_pawn)
            white_pawn.set_pos((x, 1))
        for x, piece in enumerate(self.pieces[util.PlayerColor.Black][0:8]):
            self.squares[7][x].place_piece(piece)
            piece.set_pos((x, 7))
        for x, black_pawn in enumerate(self.pieces[util.PlayerColor.Black][8:16]):
            self.squares[6][x].place_piece(black_pawn)
            black_pawn.set_pos((x, 6))
