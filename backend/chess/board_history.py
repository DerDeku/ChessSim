from . import Board
from collections import deque

class BoardHistory:
    def __init__(self, fresh_board: Board):
        self._storage = deque()
        self.turn = 0
        self._fresh_board = fresh_board.get_copy()
        
    def set_fresh_board(self, board: Board) -> None:
        self._fresh_board = board.get_copy()
        
    def add_turn(self, board: Board) -> None:
        self._storage.append(board.get_copy())
        self.turn += 1
    
    def go_back(self, half_turns: int = 1) -> Board:
        for _ in range(half_turns):
            if len(self._storage) >= 1:
                self._storage.pop()
        return self._storage.pop() if len(self._storage) >= 1 else self._fresh_board.get_copy()