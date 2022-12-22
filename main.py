from Progressive_mancala import *
from Players import *
board = Board()
player1 = Player(1, 0)
player2 = Player(2, 1)
board.host_game(player1, player2)
# print(board)