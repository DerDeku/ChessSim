from .square import Square
from .piece import Piece
from .util import to_python_indecies, PlayerColor
import os

DIMENSION = 8

class Board:
    def __init__(self):
        self.squares: list[list[Square]] = list()
        self.kings: list[Piece] = list()
        
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
            highlight_square = to_python_indecies(highlight_square_name)
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
    
    def move_to(self, start_square_pos: str | tuple, target_square_pos: str | tuple) -> None | Piece:
        start_square = self._get_square(start_square_pos)
        piece = start_square.remove_piece()
        target_square = self._get_square(target_square_pos)
        taken_piece = target_square.place_piece(piece)
        return taken_piece
        
    def get_piece(self, square: str | tuple) -> Piece:
        if isinstance(square, str):
            x, y = to_python_indecies(square)
        else:
            x,y = square
        if self.has_piece((x,y)):
            return self.squares[y][x].content
        else:
            raise Exception(f"No piece on square {square}")
        
    def kings_to_close(self, pos_k1: tuple, pos_k2: tuple) -> bool:
        return abs(pos_k1[0]-pos_k2[0]) < 2 and abs(pos_k1[1]-pos_k2[1]) < 2
        
    def get_enemys_king_position(self, own_color: str) -> tuple:
        return self.kings[1].pos if own_color == PlayerColor.White else self.kings[0].pos
    
    def get_king_from_color(self, color: str) -> Piece:
        return self.kings[0] if color == PlayerColor.White else self.kings[1] 
    
    def _get_square(self, square: str | tuple) -> Square:
        if isinstance(square, str):
            x, y = to_python_indecies(square)
        elif isinstance(square, tuple):
            x, y = square
        return self.squares[y][x]

    def has_piece(self, square: str | tuple[int, int]) -> bool:
        if isinstance(square, str):
            x, y = to_python_indecies(square)
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
        self.pieces: list[Piece] = list()
        for color in [Piece.Color.White, Piece.Color.Black]:
            self.pieces.append(Piece(Piece.Figure.Rook, color))
            self.pieces.append(Piece(Piece.Figure.Knight, color))
            self.pieces.append(Piece(Piece.Figure.Bishop, color))
            self.pieces.append(Piece(Piece.Figure.Queen, color))
            self.pieces.append(Piece(Piece.Figure.King, color))
            self.kings.append(self.pieces[-1])
            self.pieces.append(Piece(Piece.Figure.Bishop, color))
            self.pieces.append(Piece(Piece.Figure.Knight, color))
            self.pieces.append(Piece(Piece.Figure.Rook, color))
            for _ in range(8):
                self.pieces.append(Piece(Piece.Figure.Pawn, color))
                
    def _place_pieces(self) -> None:        
        for x, piece in enumerate(self.pieces[0:8]):
            self.squares[0][x].place_piece(piece)
            piece.set_pos((x, 0))
        for x, white_pawn in enumerate(self.pieces[8:16]):
            self.squares[1][x].place_piece(white_pawn)
            white_pawn.set_pos((x, 1))
        for x, black_pawn in enumerate(self.pieces[24:32]):
            self.squares[6][x].place_piece(black_pawn)
            black_pawn.set_pos((x, 6))
        for x, piece in enumerate(self.pieces[16:24]):
            self.squares[7][x].place_piece(piece)
            piece.set_pos((x, 7))