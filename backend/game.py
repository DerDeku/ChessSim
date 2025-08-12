from datetime import datetime
from .board import Board
from .piece import Piece
from .moveCalculator import MoveCalculator
from .util import X_LINE, to_python_indecies, PlayerColor, PGN_win
from .san import San
import os

class Game:
    def __init__(self) -> None:
        self.setup_pgn_info()
        self.moves: list[str]   = list()
        self.board: Board       = Board()
        self.San: San           = San()
        self.move_calculator    = MoveCalculator(self.board)
        self.checkmate          = False
        self.check              = False
        
    def setup_pgn_info(self) -> None:
        self.en_passant = "-"
        self.half_turns_since_event = 0 # pawn moved or piece taken
        self.turn = 1
        self.color_to_move = PlayerColor.White
        self.castings_still_possible = "KQkq"
        self.date = datetime.now().isoformat()
        self.tournament = "None"
        self.site = "Germany"
        self.round = 1
        self.white_playername = "Jo"
        self.black_playername = "Auch Jo"
        self.result = "*" # 1-0 = white won, 0-1 = black won, 1/2-1/2 = remis, * inclomplete
    
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
                if self.checkmate:
                    self.end_game()
                    break
                else:
                    self.end_turn()
    
    def play_turn(self) -> bool:
        self.board.show_board()
        square_name = self.select_piece()
        valid_moves = self.move_calculator.validMoves(square_name)        
        self.board.show_board(valid_moves, square_name)
        target_square_name = self.select_move(valid_moves)
        if target_square_name is None:
            return False
        taken_piece = self.board.move_to(square_name, target_square_name)
        piece_name = self.board.get_piece(target_square_name)
        self.board.show_board()
        self.check = self.is_check()
        # TODO: check en passant, checkmate, conversion
            
        self.San.add(piece_name, square_name, target_square_name, self.board, taken_piece, check=self.check, check_mate=self.checkmate)
        return True
    
    def is_check(self) -> bool:
        if self.color_to_move is PlayerColor.White:
            king = self.board.kings[1]
        else:
            king = self.board.kings[0]
        return self.move_calculator.king_under_attack(king.pos, king)

    def can_king_move(self) -> bool:
        if self.color_to_move is PlayerColor.White:
            king = self.board.kings[1]
        else:
            king = self.board.kings[0]
        return self.move_calculator.validMoves(piece=king)
            
    def end_game(self) -> None:
        self.result = PGN_win[self.color_to_move]
        os.system("cls")
        self.board.show_board()
        print("Checkmate - " + self.color_to_move + " won")
    
    def end_turn(self) -> None:
        if self.color_to_move == PlayerColor.White:
            self.color_to_move = PlayerColor.Black
        
        else:
            self.color_to_move = PlayerColor.White
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
        line = f"-- {self.color}'s move --"
        if self.check:
            line += " CHECK"
        print(line)
        print("select piece to move")
        while True:
            square = input()
            if not self.is_good(square):
                continue
            if not self.board.has_piece(square):
                print(f"square {square} has no piece")
                continue
            if not self.board.get_piece(square).is_color(self.color_to_move):
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
