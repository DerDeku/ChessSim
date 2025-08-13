from datetime import datetime
import os

from . import Board
from . import Piece
from . import util
from ..moveCalculation.moveCalculator import MoveCalculator
from ..san import San
from ..ai.bruteForce.bruteForce import BruteForce

PVP = True

class Game:
    def __init__(self) -> None:
        self.setup_pgn_info()
        self.moves: list[str]   = list()
        self.board: Board       = Board()
        self.board.setup_board()
        self.San: San           = San()
        self.move_calculator    = MoveCalculator(self.board)
        self.ai                 = BruteForce(self.board)
        self.checkmate          = False
        
    def setup_pgn_info(self) -> None:
        self.en_passant = "-"
        self.half_turns_since_event = 0 # pawn moved or piece taken
        self.turn = 1
        self.color_to_move = util.PlayerColor.White
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
        while True:
            if not PVP and self.color_to_move == util.PlayerColor.Black:
                if not self.ai_turn():
                    return
            if not self.play_turn():
                continue
            if not self.end_turn():
                return
        
    def ai_turn(self) -> None:
        move = self.ai.get_move()
        self.board.move_to(move[0], move[1])
        return self.end_turn()
    
    def play_turn(self) -> bool:
        self.board.show_board()
        self.board.en_passant = None
        can_move = self.move_calculator.calc_all_valid_moves(self.board.pieces[self.color_to_move])
        if not can_move and self.is_check():
            self.checkmate = True
            return True
    
        square_name = self.input_piece()
        valid_moves = self.move_calculator.get_possible_moves(square_name)        
        self.board.show_board(valid_moves, square_name)
        target_square_name = self.input_move(valid_moves)
        if target_square_name is None:
            return False
        taken_piece = self.board.move_to(square_name, target_square_name)
        piece = self.board.get_piece(target_square_name)
        if piece.name == Piece.Figure.Pawn:
            self.handle_pawn(piece)
        # TODO: check/checkmate
        self.board.show_board()
        check_mate = False #self.is_checkmate()
            
        self.San.add(piece, square_name, target_square_name, self.board, taken_piece, check_mate=check_mate)
        return True
    
    def handle_pawn(self, piece: Piece) -> None:
        self.handle_en_passant()
        self.handle_promotion(piece)
        
    def handle_en_passant(self) -> None:          
        self.en_passant = util.to_chess_notation(self.board.en_passant) if self.board.en_passant else "-"
        
    def handle_promotion(self, pawn: Piece) -> None:
        if self.board.can_pawn_promote(pawn):
            self.board.show_board()
            pawn.promote_to(self.input_promotion(pawn))
    
    def is_check(self) -> bool:
        if self.color_to_move is util.PlayerColor.White:
            king = self.board.kings[1]
        else:
            king = self.board.kings[0]
        return self.move_calculator.king_under_attack()
            
    def end_game(self) -> None:
        self.result = util.PGN_win[self.color_to_move]
        self.board.show_board()
        print(f"Checkmate - {util.full_color(self.color_to_move)} lost!")
    
    def end_turn(self) -> None:
        if self.checkmate:
            return False
            
        elif self.color_to_move == util.PlayerColor.White:
            self.color_to_move = util.PlayerColor.Black
        
        else:
            self.color_to_move = util.PlayerColor.White
            self.moves.append(self.San.get_turn(self.turn))
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
    
    def input_move(self, valid_moves: list[tuple]) -> str:
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

    def input_piece(self) -> None:
        print(f"-- {self.color}'s move --\n")
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
