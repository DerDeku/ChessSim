from .square import Square
from .piece import Piece
from .util import to_python_indecies

DIMENSION = 8

class Board:
    def __init__(self):
        self.squares: list[list[Square]] = list()
        
    def as_fen(self) -> str:
        pass # TODO return board in FEN format: "rnbqkbnr/pppppppp/8/8/8/8/pppppppp/rnbqkbnr"
    
    def setup_board(self) -> None:
        self._create_board()
        pieces = self._create_pieces()
        self._place_pieces(pieces)
        
    def show_board(self, highlights: list[tuple] = None) -> None:
        for y, y_line in enumerate(reversed(self.squares)):
            y = len(self.squares) - y
            print_line = f"{y}    "
            for x, square in enumerate(y_line):
                if highlights and (x,y-1) in highlights:
                    print_line += " "
                    print_line += self.color_line(square.content, "red")
                    print_line += " "
                else:
                    print_line += f" {square.content} "
            print(print_line)
        print("\n      A  B  C  D  E  F  G  H\n")
        
    def color_line(self, line: str, color: str) -> str:
        prefix = "\033"
        color = "[31m" # red
        suffix = "\033[0m"
        return f"{prefix}{color}{line}{suffix}"
        
        
    def get_piece(self, square: str) -> Piece:
        if self.has_piece(square):
            x, y = to_python_indecies(square)
            return self.squares[y][x].content
        else:
            raise Exception(f"No piece on square {square}")

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
                
    def _create_pieces(self) -> None:
        pieces = list()
        for color in [Piece.Color.White, Piece.Color.Black]:
            pieces.append(Piece(Piece.Figure.Rook, color))
            pieces.append(Piece(Piece.Figure.Knight, color))
            pieces.append(Piece(Piece.Figure.Bishop, color))
            pieces.append(Piece(Piece.Figure.King, color))
            pieces.append(Piece(Piece.Figure.Queen, color))
            pieces.append(Piece(Piece.Figure.Bishop, color))
            pieces.append(Piece(Piece.Figure.Knight, color))
            pieces.append(Piece(Piece.Figure.Rook, color))
            for _ in range(8):
                pieces.append(Piece(Piece.Figure.Pawn, color))
        return pieces
                
    def _place_pieces(self, pieces: list[Piece]) -> None:        
        for x, piece in enumerate(pieces[0:8]):
            self.squares[0][x].place_piece(piece)
        for x, white_pawn in enumerate(pieces[8:16]):
            self.squares[1][x].place_piece(white_pawn)
        for x, black_pawn in enumerate(pieces[24:32]):
            self.squares[6][x].place_piece(black_pawn)
        for x, piece in enumerate(pieces[16:24]):
            self.squares[7][x].place_piece(piece)