from ..ai import Ai
from ...chess import util
class BruteForce(Ai):
    def __init__(self, board) -> None:
        super().__init__(board)
        self.best_variant = None

    def set_depth(self, depth: int) -> None:
        self.depth = depth

    def get_move(self) -> tuple[str]:
        """Returns tuple of two strings: tuple[0] start pos, tuple[1] target pos"""
        move = self.calc_variants(list())
        return move
    
    def evalue_variant(self, board) -> int:
        pass
    
    def calc_variants(self, variants: list[dict]) -> list[dict]:
        """Returns a variant """
        original_board = self.board.get_copy()
        depth = 0
        is_enemy_turn = False
        new_variant = True
        while True:
            color = "w" if is_enemy_turn else "b"
            if len(variants) == depth:
                variant = dict()
                ghost_board = self.board.get_copy()
                variant.setdefault(E_Variant.Board, ghost_board)
                variant.setdefault(E_Variant.MoveIndex, [0,0])
                variant.setdefault(E_Variant.PieceIndex, [0,0])
                variant.setdefault(E_Variant.MoveNotation, ["",""])
                variants.append(variant)
            if new_variant:
                variant = variants[depth]
                self.moveCalculator.use_board(self.board)
                
                piece = self.board.pieces[color][variant[E_Variant.PieceIndex][is_enemy_turn]]
                moves = self.moveCalculator._validMoves(piece=piece)
                if not moves:
                    variant[E_Variant.PieceIndex][is_enemy_turn] += 1
                    continue
                start_pos = util.to_chess_notation(piece.pos)
                end_pos = util.to_chess_notation(moves[variant[E_Variant.MoveIndex][is_enemy_turn]])
                variant[E_Variant.MoveNotation][is_enemy_turn] = (start_pos, end_pos)
            self.board.move_to(*variant[E_Variant.MoveNotation][is_enemy_turn])
            if is_enemy_turn:
                depth += 1
            if depth == self.depth: 
                return variants
            is_enemy_turn = not is_enemy_turn
            
class E_Variant:
    Board           = "board"
    MoveIndex       = "move_index"
    MoveNotation    = "move_notation"
    PieceIndex      = "piece_index"