X_LINE = ["A","B","C","D","E","F","G","H"]

class PlayerColor:
    White = "w"
    Black = "b"
    
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