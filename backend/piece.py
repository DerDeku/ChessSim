class Piece:
    class Color:
        White = "White"
        Black = "Black"

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
    
    def __str__(self): 
        return self.name.upper() if self.color == self.Color.White else self.name

    def is_color(self, color: str) -> bool:
        return color == self.color