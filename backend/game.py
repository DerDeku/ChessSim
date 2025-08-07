from datetime import datetime
from .board import Board
from .moveCalculator import validMoves
from .util import X_LINE

class Game:
    def __init__(self) -> None:
        self.board = Board()
        self.en_passant = "-"
        self.half_turns_since_event = 0 # pawn moved or piece taken
        self.turn = 1
        self.color_to_move = "b"
        self.castings_still_possible = "KQkq"
        self.date = datetime.now().isoformat()
        self.tournament = "None"
        self.site = "Germany"
        self.round = 1
        self.white_playername = "Jo"
        self.black_playername = "Auch Jo"
        self.result = "0-0" # 1-0 = white won, 0-1 = black won, 1/2-1/2 = remis
        self.moves: list[tuple[str, str, str]] = list()
    
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
        self.board.show_board()
        square = self.select_piece()
        valid_moves = validMoves(self.board, square)
        self.board.show_board(valid_moves)
        
        print()
        
    def select_piece(self) -> None:
        print(f"-- {self.color}'s move --\n\n")
        print("-- select piece to move --")
        while True:
            square = input()
            if len(square) != 2:
                print("Input must be 2 characters long! - AGAIN!")
                continue
            if square[0].capitalize() not in X_LINE:
                print(f"First character must be one of {X_LINE}")
                continue
            try:
                y = int(square[1])
                if 0 > y or y > 8:
                    print("Second character must be a number between 1 and 8")
                    continue
            except Exception as e:
                print("Second character must be a number - " + str(e))
                continue
            if not self.board.has_piece(square):
                print(f"square {square} has no piece")
                continue
            if not self.board.get_piece(square).is_color(self.color):
                print("Piece is not your color")
                continue
            square = square[0].capitalize() + square[1]
            return square