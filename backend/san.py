from .board import Board
from .piece import Piece
from .util import to_python_indecies, to_chess_notation, X_LINE

class San:
    def __init__(self):
        self.san = ""

    def add(self, piece: Piece, start_pos: str, end_pos: str, board: Board, taken_piece_name: str | None = None, cconversion_name: str | None = None, check: bool = False, check_mate: bool = False):
        figure_name = piece.name.capitalize()
        disambiguation = None
        takes = ""
        target_field = end_pos.lower()
        conversion = ""
        _check = ""
        _check_mate = ""

        if figure_name == Piece.Figure.Pawn.capitalize():
            figure_name = ""
        
        disambiguation = self.check_disambiguation(start_pos, end_pos, board)

        if taken_piece_name:
            takes = "x"
        
        if cconversion_name:
            conversion = "=" + cconversion_name.capitalize()
        
        if check:
            _check = "+"

        elif check_mate:
            _check_mate = "#"
        
        self.san += f" {figure_name}{disambiguation}{takes}{target_field}{conversion}{_check}{_check_mate}"

    def get_turn(self, turn: int) -> str:
        san = f"{turn}.{self.san}"

        self.san = ""
        return san

    def check_disambiguation(self, start_pos: str, end_pos: str, board: Board) -> str:
        #TODO
        return ""