X_LINE = ["A","B","C","D","E","F","G","H"]

def to_chess_notation(coordinates: tuple[int, int]) -> tuple[str, str]:
    return X_LINE[coordinates[0]], coordinates[1] + 1

def to_python_indecies(square: str) -> tuple[int, int]:
    return X_LINE.index(square[0].upper()), int(square[1]) - 1 