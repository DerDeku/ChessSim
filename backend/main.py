from .chess.game import Game

def main() -> None:
    run_game()

def run_game() -> None:
    game = Game()
    game.start()
    game.end_game()