class Piece:
    class Color:
        White = "w"
        Black = "b"

    class Figure:
        King    = "k"
        Queen   = "q"
        Knight  = "n"
        Bishop  = "b"
        Rook    = "r"
        Pawn    = "p"

    def __init__(self, name: str, color: str):
        self.name = name
        self.color = color
        self._pos = None
    
    def __str__(self): 
        return self.name.upper() if self.color == self.Color.White else self.name

    def is_color(self, color: str) -> bool:
        return color == self.color
    
    @property
    def pos(self) -> tuple:
        return self._pos
    
    def set_pos(self, pos: tuple) -> None:
        self._pos = pos