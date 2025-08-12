from ..moveCalculation.moveCalculator import MoveCalculator
from ..chess import Board

class Ai:
    def __init__(self, board: Board):
        self.board = board.get_copy()
        self.moveCalculator = MoveCalculator(board)
        self.depth = 4
        
    def get_move(self):
        """Should return a move as a string in Standard Algebraic Notaion"""
        pass