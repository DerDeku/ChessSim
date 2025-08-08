from .util import to_chess_notation
from .piece import Piece

class Square:
    def __init__(self) -> None:
        self._x: int 
        self._y: int 
        self._name: tuple[str]
        self._content: Piece = None
    
    def __str__(self) -> str:
        return str(f"{self._name} : {self._content}")
    
    def set_pos(self, x : int, y: int) -> None:
        if 0 <= x < 8 and 0 <= y < 8:
            self._x = x
            self._y = y
            self._name = to_chess_notation((x,y))
        else:
            raise Exception("Coordinates have no valid value")
    
    def pos(self, chess_notation: bool = False) -> tuple:
        if chess_notation:
            return to_chess_notation((self._x, self._y))
        else:
            return self._x, self._y
    
    @property
    def name(self) -> tuple[str]:
        return self._name
    
    @property
    def content(self) -> Piece | str:
        return self._content if self._content else "."
    
    def place_piece(self, piece: Piece) -> None | Piece:
        taken_piece = None
        if self._content:
            taken_piece = self._content

        self._content = piece
        piece.set_pos(self.pos())
        return taken_piece
        
    def take_piece(self, piece: Piece) -> None:
        if self._content:
            self._content = piece
        else:
            raise Exception("Can not take a piece from this square: no piece on square | use function: place_piece()")
    
    def remove_piece(self) -> Piece:
        if self._content:
            content = self._content
            self._content = None
            return content
        else:
            raise Exception("Can not remove piece from this square: no piece on square")
    
        