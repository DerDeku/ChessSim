from ..chess import Board
from ..chess import Piece
from ..chess import util

class PositionEvaluator:
    def __init__(self):
        self.piece_values = {   Piece.Figure.Pawn : 1,
                                Piece.Figure.Knight : 3,
                                Piece.Figure.Bishop : 3,
                                Piece.Figure.Rook : 5,
                                Piece.Figure.Queen : 9,
                                Piece.Figure.King : 0}

    def evaluate_current_position(self, board: Board) -> int:
        """Evaluates current position of the board.A positive value means White has an advantage while a negative means black has an advantage"""
        value = self._get_piece_value_evaluation(board)
        return value
    
    def _get_piece_value_evaluation(self, board: Board) -> int:    
        white_pieces = board.get_pieces(util.PlayerColor.White)
        white_value = self._value_of_pieces(white_pieces)
        black_pieces = board.get_pieces(util.PlayerColor.Black)
        black_value = self._value_of_pieces(black_pieces)
        return white_value-black_value
    
    def _value_of_pieces(self, pieces: list[Piece]) -> int:
        value = 0
        for piece in pieces:
            value += self.piece_values[piece.name]
        return value 
