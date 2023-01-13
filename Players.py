from Board import *
import random

class Player:
    # HUMAN = 0
    # RANDOM = 1
    def __init__(self, player_num, player_type, ply = 0):
        """Initializes the players."""
        self.HUMAN = 0
        self.RANDOM = 1
        self.num = player_num
        self.opp = 2 - player_num + 1
        self.type = player_type
        self.ply = ply

    def __repr__(self):
        """Represents this object - returns the player's number."""
        return str(self.num)

    def score(self, board):
        if board.has_won(self.num):
            return 1
        elif board.has_won(self.opp):
            return -1
        else:
            return 0

    def choose_move(self, board):
        """Accepts moves from a 'HUMAN' player or else generates random moves if it is a 'RANDOM' player."""
        if self.type == self.HUMAN:
            while True:
                try:
                    move = int(input("Enter Your Move"))
                except ValueError:
                    print("Please Enter a valid move")
                else:
                    break

            while not board.is_legal_move(self, move):
                print("Your move is not valid")
                break
            return move
        # random generation
        if self.type == self.RANDOM:
            move = random.choice(board.get_legal_moves(self))
            print(f'{move} has been chosen')
            return move
        
    def miniMaxMove(self, board, depth, max_for_player):
        """Maximizes the minimum score possible by playing a move, returns tuple of best move."""
        if depth == 0 or board.is_game_over():
            return None, board.get_score(max_for_player)

        moves = board.get_possible_moves(self)
        print(f"moves => {moves}")
        maximise = max_for_player == self
        worst_score = float('-inf') if maximise else float('inf')
        best_move = moves[0], worst_score

        for move in moves:
            next_state = board.future_lookup(self, move)
            new_board, player = next_state
            # recursive call for depth times
            _, score = self.miniMaxMove(player, new_board, depth - 1, max_for_player)

            set_new_max = maximise and score >= best_move[1]
            set_new_min = (not maximise) and score <= best_move[1]
            if set_new_max or set_new_min:
                best_move = move, score
        return best_move
