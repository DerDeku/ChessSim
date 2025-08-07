from datetime import datetime
from .board import Board
from .piece import Piece
from .moveCalculator import validMoves
from .util import X_LINE, to_python_indecies
from .san import San
import os

class Game:
    def __init__(self) -> None:
        self.board = Board()
        self.en_passant = "-"
        self.half_turns_since_event = 0 # pawn moved or piece taken
        self.turn = 1
        self.color_to_move = "w"
        self.castings_still_possible = "KQkq"
        self.date = datetime.now().isoformat()
        self.tournament = "None"
        self.site = "Germany"
        self.round = 1
        self.white_playername = "Jo"
        self.black_playername = "Auch Jo"
        self.result = "0-0" # 1-0 = white won, 0-1 = black won, 1/2-1/2 = remis, * inclomplete
        self.moves: list[str] = list()
        self.San = San()
    
    @property
    def color(self) -> str:
        color = {"w" : "White", "b" : "Black"}
        return color[self.color_to_move]
    
    def as_fen(self) -> str: # Forsyth-Edwards Notation
        return f"{self.board.as_fen()} {self.color_to_move} {self.castings_still_possible} {self.en_passant} {self.half_turns_since_event} {self.turn}"

    def as_pgn(self) -> dict: # Portable Game Notation
        return {"Event" : self.tournament,
                "Site"  : self.site, 
                "Date"  : self.date,
                "Round" : self.round,
                "White" : self.white_playername,
                "Black" : self.black_playername,
                "Result": self.result,
                "Moves" : self.moves}

    def start(self) -> None:
        self.board.setup_board()
        while True:
            if self.play_turn():
                self.end_turn()
    
    def play_turn(self) -> bool:
        
        self.board.show_board()
        square_name = self.select_piece()
        valid_moves = validMoves(self.board, square_name)
        
        self.board.show_board(valid_moves)
        target_square_name = self.select_move(valid_moves)
        if target_square_name is None:
            return False
        taken_piece = self.board.move_to(square_name, target_square_name)
        piece_name = self.board.get_piece(target_square_name)
        # TODO: check en passant, check/checkmate, conversion
        self.board.show_board()
        self.San.add(piece_name, square_name, target_square_name, self.board, taken_piece)
        return True
    
    def end_turn(self) -> None:
        if self.color_to_move == "w":
            self.color_to_move = "b"
        
        else:
            self.color_to_move = "w"
            self.moves.append(self.San.get_turn(self.turn))
            self.turn += 1

    def select_move(self, valid_moves: list[tuple]) -> str:
        print(f"-- {self.color}'s move --\n")
        print("select where to move")
        print("'x' to abort")
        while True:
            move_to = input()
            if move_to == "x" or move_to == "X":
                return None
            if not self.is_good(move_to):
                continue
            if to_python_indecies(move_to) not in valid_moves:
                print(f"Your input {move_to} is no valid option")
                continue
            return move_to

    def select_piece(self) -> None:
        print(f"-- {self.color}'s move --\n")
        print("select piece to move")
        while True:
            square = input()
            if not self.is_good(square):
                continue
            if not self.board.has_piece(square):
                print(f"square {square} has no piece")
                continue
            if not self.board.get_piece(square).is_color(self.color):
                print("Piece is not your color")
                continue
            square = square[0].capitalize() + square[1]
            return square
        
    def is_good(self, input) -> bool:
        if len(input) != 2:
            print("Input must be 2 characters long! - AGAIN!")
            return False
        if input[0].capitalize() not in X_LINE:
            print(f"First character must be one of {X_LINE}")
            return False
        try:
            y = int(input[1])
            if 0 > y or y > 8:
                print("Second character must be a number between 1 and 8")
                return False
        except Exception as e:
            print("Second character must be a number - " + str(e))
            return False
        return True
