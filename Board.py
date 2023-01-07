from Players import *

class Board:
    def __init__(self):
        """Initializes the Board."""
        self.reset()

    def reset(self):
        """Resets all the variants of the Board."""
        self.PITS = 6
        self.PLAYER1_PITS = [4] * self.PITS
        self.PLAYER2_PITS = [4] * self.PITS
        self.bankPits = [0, 0]

    def __repr__(self):
        """Custom repr() method to represent this object."""
        ret = "P L A Y E R  2\n"
        ret += "------------------------------------------------------------\n"
        ret += str(self.bankPits[1]) + "\t"
        for elem in range(len(self.PLAYER2_PITS) - 1, -1, -1):
            ret += str(self.PLAYER2_PITS[elem]) + "\t"
        ret += "\n\t"
        for elem in self.PLAYER1_PITS:
            ret += str(elem) + "\t"
        ret += str(self.bankPits[0])
        ret += "\n------------------------------------------------------------"
        ret += "P L A Y E R  1\n"
        return ret

    def is_legal_move(self, player, pit):
        """Return the legality of the proposed move 'pit' by the player 'player'."""
        if player.num == 1:
            pits = self.PLAYER1_PITS
        else:
            pits = self.PLAYER2_PITS
        return 0 < pit <= len(pits) and pits[pit-1] != 0

    def is_game_over(self):
        """Returns True if the game has ended."""
        end = True
        for j in range(len(self.PLAYER1_PITS)):
            if self.PLAYER1_PITS[j] != 0:
                end = False
        if end:
            return True
        for k in range(len(self.PLAYER2_PITS)):
            if self.PLAYER2_PITS[k] != 0:
                end = False
        if end:
            return True

    def has_won(self, player):
        """Returns 'True' if the player 'player' wons the game or not."""
        if self.is_game_over():
            opp_player = 2 - player + 1
            return self.bankPits[player -1] > self.bankPits[opp_player - 1]
        else:
            return False

    def get_possible_moves(self, player):
        """Return the list of possible moves in accordance with the rules of the game."""
        if player.num == 1:
            pits = self.PLAYER1_PITS
        else:
            pits = self.PLAYER2_PITS
        possible_moves = []
        # book non-zero pits (possible moves)
        for i in range(len(pits)):
            if pits[i] != 0:
                possible_moves.append(i+1)
        return possible_moves

    def move_helper(self, player, pit):
        """Helper function for the 'make_move' method, returns a boolean for repeating a turn."""
        if player.num == 1:
            pits = self.PLAYER1_PITS
            opp_pits = self.PLAYER2_PITS
        else:
            pits = self.PLAYER2_PITS
            opp_pits = self.PLAYER1_PITS
        init_pits = pits
        stones = pits[pit-1]
        pits[pit-1] = 0
        pit += 1
        repeat_turn = False
        while stones > 0:
            repeat_turn = False
            # seeding stones into pits
            while pit <= len(pits) and stones > 0:
                pits[pit-1] += 1
                stones -= 1
                pit += 1
            if stones == 0:
                break
            if pits == init_pits: # ??
                self.bankPits[player.num - 1] += 1
                stones -= 1
                repeat_turn = True
            pits, opp_pits = opp_pits, pits
            pit = 1
        if repeat_turn:
            return True

        if pits == init_pits and pits[pit - 2] == 1:
            self.bankPits[player.num - 1] += opp_pits[(self.PITS - pit) + 1]
            opp_pits[(self.PITS - pit) + 1] = 0
            pits[pit - 2] = 0
        return False

    def make_move(self, player, pit):
        """Makes the actual move in the game - returns whether the game can continue or not."""
        repeat = self.move_helper(player, pit)
        if self.is_game_over(): # If the game has ended
            for i in range(len(self.PLAYER1_PITS)):
                self.bankPits[0] += self.PLAYER1_PITS[i]
                self.PLAYER1_PITS[i] = 0
            for j in range(len(self.PLAYER2_PITS)):
                self.bankPits[1] += self.PLAYER2_PITS[j]
                self.PLAYER2_PITS[j] = 0
            return False
        else:
            return repeat

    def get_score(self, player):
        """Return the running score of the player 'player'."""
        return self.bankPits[player.num -1]

    def host_game(self, player1, player2):
        """Hosts the game"""
        self.reset()
        curr_player = player1
        wait_player = player2
        # main loop of the game - continues until it ends
        while not (self.is_game_over()):
            again = True
            while again:
                print(self)
                move = curr_player.choose_move(self)
                # validate the chosen move
                while not (self.is_legal_move(curr_player, move)):
                    print(f"{move} is not legal")
                    move = curr_player.choose_move(self)
                again = self.make_move(curr_player, move)
            curr_player, wait_player = wait_player, curr_player
        # End message
        print(self)
        if self.has_won(curr_player.num):
            print(f"Player {curr_player} wins with score {self.get_score(curr_player)}")

        elif self.has_won(wait_player.num):
            print(f"Player {wait_player} wins with score {self.get_score(curr_player)}")
        else:
            print("Tie Game")
