from Board import *
from Players import *

def main():
    """The main entry of the game."""
    board = Board()
    player1 = Player(1, 0)
    player2 = Player(2, 1)
    board.host_game(player1, player2)

if __name__ == "__main__":
    main()
