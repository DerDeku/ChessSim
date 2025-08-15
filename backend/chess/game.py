from datetime import datetime
import os
from enum import Enum

from . import Board
from . import Piece
from . import util
from . import BoardHistory
from ..moveCalculation.moveCalculator import MoveCalculator
from ..ai.bruteForce.bruteForce import BruteForce

PVP = True

class Game:
    def __init__(self) -> None:
        self.setup_pgn_info()
        self.moves: list[str]   = list()
        self.board: Board       = Board()
        self.board.setup_board()
        self.move_calculator    = MoveCalculator()
        self.ai                 = BruteForce(self.board)
        self.checkmate          = False
        self.board_history      = BoardHistory(self.board)
        
    def setup_pgn_info(self) -> None:
        self.en_passant = "-"
        self.half_turns_since_event = 0 # pawn moved or piece taken
        self.turn = 1
        self.castings_still_possible = "KQkq"
        self.date = datetime.now().isoformat()
        self.tournament = "None"
        self.site = "Germany"
        self.round = 1
        self.white_playername = "Jo"
        self.black_playername = "Auch Jo"
        self.result = "*" # 1-0 = white won, 0-1 = black won, 1/2-1/2 = remis, * inclomplete
    
    def ai_turn(self) -> None:
        move = self.ai.get_move()
        self.board.handle_move(move[0], move[1])
        self.board.end_turn()
        return self.end_turn()

    def start(self) -> None:
        while True:
            if not PVP and self.ai.playing_as_color == self.board.color_to_move:
                next_turn = self.ai_turn()
                if not next_turn:
                    break
                
            done = self.play_turn()
            if not done: # Repeat turn
                continue

            next_turn = self.end_turn()
            if not next_turn: # Game Over
                break
        
    def debug_go_back(self, square_name: str) -> str:
        if square_name == "X":
            self.board = self.board_history.go_back()
            return True
        else:
            return False
        
    def get_where_to_move_piece(self, square_name: str) -> str | None:
        piece = self.board.get_piece(square_name)
        valid_moves = self.move_calculator.get_possible_moves(piece)        
        self.board.show_board(valid_moves, square_name)
        return self.input_move(valid_moves)

    def handle_moving_piece_to(self, square_name: str, target_square_name) -> tuple[Piece]:
        taken_piece = self.board.handle_move(square_name, target_square_name)

    def play_turn(self) -> bool:
        """Return 'False' to repeat turn. Return 'True' to end turn"""
        if self.lost_game():
            return True
        origin_square_name = self.input_piece()
        if self.debug_go_back(origin_square_name):
            return True
        target_square_name = self.get_where_to_move_piece(origin_square_name)
        if target_square_name is None:
            return False
        self.handle_moving_piece_to(origin_square_name, target_square_name)
        self.board.end_turn()
        return True
    
    def handle_pawn(self, piece: Piece) -> None:
        self.handle_en_passant()
        self.handle_promotion(piece)
        
    def handle_en_passant(self) -> None:          
        self.en_passant = util.to_chess_notation(self.board.en_passant) if self.board.en_passant else "-"
        
    def handle_promotion(self, pawn: Piece) -> None:
        if self.board.can_pawn_promote(pawn):
            pawn.promote_to(self.input_promotion(pawn))
    
    def is_check(self) -> bool:
        king = self.board.get_king_from_color(self.board.color_to_move)
        return self.move_calculator.king_under_attack(king)
            
    def end_game(self) -> None:
        self.board.show_board()
        self.result = util.PGN_win[self.board.color_to_move]
        print(f"Checkmate - {util.full_color(self.board.color_to_move)} lost!")
    
    def end_turn(self) -> None:
        if self.checkmate:
            return False
            
        self.board_history.add_turn(self.board)
        
        if self.board.color_to_move == util.PlayerColor.White:
            self.turn += 1
        return True

    def input_promotion(self, piece: Piece) -> Piece.Figure:
        self.display_promotion_message(piece)
        promote_to = self.promote_to_queen()
        if promote_to is None:
            self.display_promotion_message(piece)
            promote_to = self.promote_to_piece()
        return promote_to
    
    def display_promotion_message(self, piece: Piece) -> None:
        os.system("cls")
        self.board.show_board()
        print(f"-- Pawn reached backrank at {util.to_chess_notation(piece.pos)} --\n")
    
    def promote_to_queen(self) -> Piece.Figure | None:
        while True:
            print("Promote to Queen? (y/n) (No = choose another piece)")
            answer = input().strip().lower()
            if answer == "y":
                return Piece.Figure.Queen
            elif answer == "n":
                return None
            else:
                print(f"Error! Your input {answer} is not valid. Please enter 'y' or 'n'")
    
    def promote_to_piece(self) -> Piece.Figure | None:
        while True:
            print("Promote to:\nq - Queen\nr - Rook\nb - Bishop\nn - Knight")
            answer = input().strip().lower()
            if answer in ["q", "n", "r", "b"]:
                return answer
            else:
                print(f"Error! Your input {answer} is not valid.\n")

    def lost_game(self) -> bool:
        can_move = self.move_calculator.calc_all_valid_moves(self.board)
        if not can_move and self.is_check():
            self.checkmate = True
            return True
    
    def input_move(self, valid_moves: list[tuple]) -> str | None:
        """Return selected square to move to or 'x' : abort"""
        print(f"-- {self.color}'s move --\n")
        print("select where to move")
        print("'x' to abort")
        while True:
            move_to = input()
            if move_to == "x" or move_to == "X":
                return None
            if not self.is_good(move_to):
                continue
            if util.to_python_indecies(move_to) not in valid_moves:
                print(f"Your input {move_to} is no valid option")
                continue
            return move_to

    def input_piece(self) -> str:
        self.board.show_board()
        print(f"-- {self.color}'s move --\n")
        print("select piece to move")
        while True:
            square = input()
            if square == "X":
                return square
            if not self.is_good(square):
                continue
            if not self.board.has_piece(square):
                print(f"square {square} has no piece")
                continue
            if not self.board.get_piece(square).is_color(self.board.color_to_move):
                print("Piece is not your color")
                continue
            square = square[0].capitalize() + square[1]
            return square
        
    def is_good(self, input: list[str]) -> bool:
        if len(input) != 2:
            print("Input must be 2 characters long! - AGAIN!")
            return False
        if input[0].capitalize() not in util.X_LINE:
            print(f"First character must be one of {util.X_LINE}")
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

    @property
    def color(self) -> str:
        color = {"w" : "White", "b" : "Black"}
        return color[self.board.color_to_move]
    
    def as_fen(self) -> str: # Forsyth-Edwards Notation
        return f"{self.board.as_fen()} {self.board.color_to_move} {self.castings_still_possible} {self.en_passant} {self.half_turns_since_event} {self.turn}"

    def as_pgn(self) -> dict: # Portable Game Notation
        return {"Event" : self.tournament,
                "Site"  : self.site, 
                "Date"  : self.date,
                "Round" : self.round,
                "White" : self.white_playername,
                "Black" : self.black_playername,
                "Result": self.result,
                "Moves" : self.moves}
