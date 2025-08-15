from enum import Enum

X_LINE = ["A","B","C","D","E","F","G","H"]

class PlayerColor:
    White = "w"
    Black = "b"
    def opponent(color) -> str:
        if color not in [PlayerColor.White, PlayerColor.Black]:
            raise Exception(f"{color} not of Type PlayerColor")
        return PlayerColor.White if color == PlayerColor.Black else PlayerColor.Black
    
def full_color(color) -> str:
    if color == PlayerColor.White:
        return "White"
    elif color == PlayerColor.Black:
        return "Black"

def to_chess_notation(coordinates: tuple) -> tuple:
    return X_LINE[coordinates[0]] + str(coordinates[1] + 1)

def to_python_indecies(square: str) -> tuple[int, int]:
    return X_LINE.index(square[0].upper()), int(square[1]) - 1 

PGN_win = {PlayerColor.White: "1-0", PlayerColor.Black : "0-1", None: "1/2-1/2"}

class CastlingRight(Enum):
    QueenSide = 2
    KingSide = 6

rook_castling_start_position = {CastlingRight.KingSide: 7, CastlingRight.QueenSide: 0}
rook_castling_end_position = {CastlingRight.KingSide: 5, CastlingRight.QueenSide: 3}
color_home_rank = {PlayerColor.White: 0, PlayerColor.Black: 7}

def get_castling_side(pos: tuple[int]) -> CastlingRight | None:
    try:
        side = CastlingRight(pos[0])
    except Exception as _:
        side = None
    return side