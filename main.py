from Board import *
from Players import *

def main():
    """The main entry of the game."""
    board = Board()
    human_player = Player(1, 0)
    # random_player = Player(2, 1)
    AI_player = Player(2, 2)
    board.host_game(human_player, AI_player)

if __name__ == "__main__":
    main()
