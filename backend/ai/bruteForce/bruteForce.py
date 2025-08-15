from ..ai import Ai
from ...positionEvaluator.posititionEvaluator import PositionEvaluator
from ...chess import util
from ...chess import Board



class BruteForce(Ai):
    def __init__(self, board, color: util.PlayerColor = util.PlayerColor.Black) -> None:
        super().__init__(board)
        self.best_variant = None
        self.best_variant_value = 0
        self.playing_as_color = color
        self.variant_board = None
        self.evaluator = PositionEvaluator()
        self.current_depth = 0
        self.max_depth = 2

    def set_depth(self, depth: int) -> None:
        self.max_depth = depth

    def get_move(self) -> tuple[str]:
        """Returns tuple of two strings: tuple[0] start pos, tuple[1] target pos"""
        self.moves = list()
        self._calc(self.board.get_copy())
        return self.best_variant
    
    def _calc(self, board: Board) -> list[dict]:
        pieces = board.get_pieces(self.board.color_to_move)
        self.moveCalculator.calc_all_valid_moves(pieces)
        for piece in pieces:
            possible_moves = self.moveCalculator.get_possible_moves(piece=piece)
            for variant in possible_moves:
                start_pos = piece.pos
                board.handle_move(start_pos, variant)
                    
                if len(self.moves) == self.current_depth:
                    self.moves.append((start_pos, variant))
                else:
                    self.moves[self.current_depth] = (start_pos, variant)
                    
                self.current_depth += 1
                if self.current_depth < self.max_depth * 2:
                    
                    self._calc(board)
                else:
                    value = self._evalue_variant(board)
                    if value > self.best_variant_value or self.best_variant is None:
                        self.best_variant = self.moves[0]
                
    def _evalue_variant(self, board) -> int:
        value = self.evaluator.evaluate_current_position(board)
        if self.playing_as_color == util.PlayerColor.Black:
            value = -value
        return value