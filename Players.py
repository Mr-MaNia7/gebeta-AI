from Progressive_mancala import *
import random

class Player:

    HUMAN = 0
    RANDOM = 1

    def __init__(self, player_num, player_type, ply = 0):
        self.num = player_num
        self.opp = 2 - player_num + 1
        self.type = player_type
        self.ply = ply

    def __repr__(self):
        return str(self.num)

    def score(self, board):
        if board.has_won(self.num):
            return 1
        elif board.has_won(self.opp):
            return -1
        else:
            return 0

    def choose_move(self, board):
        if self.type == self.HUMAN:
            while True:
                try:
                    move = int(input("Enter Your Move"))
                except ValueError:
                    print("Please Enter a valid move")
                else:
                    break

            while not board.legal_move(self, move):
                print("Your move is not valid")
                break
            return move
        if self.type == self.RANDOM:
            move = random.choice(board.legal_moves(self))
            print(f'{move} has been chosen')
            return move


