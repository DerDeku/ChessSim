from .util import to_chess_notation
from .piece import Piece

class Square:
    def __init__(self) -> None:
        self._x = None
        self._y = None
        self._name = None
        self._content = None
    
    def __str__(self) -> None | Piece:
        return str(f"{self._name} : {self._content}")
    
    def set_pos(self, x : int, y: int) -> None:
        if 0 <= x < 8 and 0 <= y < 8:
            self._x = x
            self._y = y
            self._name = to_chess_notation((x,y))
        else:
            raise Exception("Coordinates have no valid value")
    
    def pos(self, chess_notation: bool = False) -> tuple[int, int]:
        if chess_notation:
            return to_chess_notation((self._x, self._y))
        else:
            return self._x, self._y
    
    @property
    def name(self) -> tuple[str, str]:
        return self._name
    
    @property
    def content(self) -> str:
        return self._content if self._content else "."
    
    def place_piece(self, piece: Piece) -> None:
        if self._content:
            raise Exception(f"Can not place piece {piece} on this square: occupied already | use function: take_piece()") 
        else:
            self._content = piece
        
    def take_piece(self, piece: Piece) -> None:
        if self._content:
            self._content = piece
        else:
            raise Exception("Can not take a piece from this square: no piece on square | use function: place_piece()")
    
    def remove_piece(self) -> None:
        if self._content:
            self._content = None
        else:
            raise Exception("Can not remove piece from this square: no piece on square")
    
        