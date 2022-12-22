import self as self

from Players import *
class Board:
    def __init__(self):
        self.reset()

    def reset(self):
        self.CUPS = 6
        self.P1CUPS = [4] * self.CUPS
        self.P2CUPS = [4] * self.CUPS
        self.scoreCups = [0, 0]

    def __repr__(self):
        ret = "P L A Y E R  2\n"
        # ret += "\t6\t5\t4\t3\t2\t1\n"
        ret += "------------------------------------------------------------\n"
        ret += str(self.scoreCups[1]) + "\t"
        for elem in range(len(self.P2CUPS) - 1, -1, -1):
            ret += str(self.P2CUPS[elem]) + "\t"
        ret += "\n\t"
        for elem in self.P1CUPS:
            ret += str(elem) + "\t"
        ret += str(self.scoreCups[0])
        ret += "\n------------------------------------------------------------"
        # ret += "\n\t1\t2\t3\t4\t5\t6\n"
        ret += "P L A Y E R  1\n"
        return ret

    def legal_move(self, player, cup):
        if player.num == 1:
            cups = self.P1CUPS
        else:
            cups = self.P2CUPS
        return (cup > 0) and (cup <= len(cups)) and (cups[cup-1] != 0)

    def legal_moves(self, player):
        if player.num == 1:
            cups = self.P1CUPS
        else:
            cups = self.P2CUPS
        moves = []
        for i in range(len(cups)):
            if cups[i] != 0:
                moves.append(i+1)
        return moves

    def move_helper(self, player, cup):
        if player.num == 1:
            cups = self.P1CUPS
            opp_cups = self.P2CUPS
        else:
            cups = self.P2CUPS
            opp_cups = self.P1CUPS
        init_cups = cups
        stones = cups[cup-1]
        cups[cup-1] = 0
        cup += 1
        repeat_turn = False
        while stones > 0:
            repeat_turn = False
            while cup <= len(cups) and stones > 0:
                cups[cup-1] += 1
                stones -= 1
                cup += 1
            if stones == 0:
                break
            if cups == init_cups:
                self.scoreCups[player.num-1] += 1
                stones -= 1
                repeat_turn = True
            temp_cups = cups
            cups = opp_cups
            opp_cups = temp_cups
            cup = 1
        if repeat_turn:
            return True

        if cups == init_cups and cups[cup - 2] == 1:
            self.scoreCups[player.num - 1] += opp_cups[(self.CUPS - cup) + 1]
            opp_cups[(self.CUPS - cup) + 1] = 0
            cups[cup - 2] = 0
        return False

    def make_move(self, player, cup):
        repeat = self.move_helper(player, cup)
        if self.game_over():
            for i in range(len(self.P1CUPS)):
                self.scoreCups[0] += self.P1CUPS[i]
                self.P1CUPS[i] = 0
            for j in range(len(self.P2CUPS)):
                self.scoreCups[1] += self.P2CUPS[j]
                self.P2CUPS[j] = 0
            return False
        else:
            return repeat

    def has_won(self, player):
        if self.game_over():
            opp_player = 2 - player + 1
            return self.scoreCups[player -1] > self.scoreCups[opp_player - 1]
        else:
            return False

    def game_over(self):
        end = True
        for j in range(len(self.P1CUPS)):
            if self.P1CUPS[j] != 0:
                end = False
        if end:
            return True
        for k in range(len(self.P2CUPS)):
            if self.P2CUPS[k] != 0:
                end = False
        if end:
            return True

    def get_score(self, player):
        return self.scoreCups[player.num -1]

    def host_game(self, player1, player2):
        self.reset()
        curr_player = player1
        wait_payer = player2
        while not (self.game_over()):
            again = True
            while again:
                print(self)
                move = curr_player.choose_move(self)
                while not (self.legal_move(curr_player, move)):
                    print(move, " is not legal")

                    move = curr_player.choose_move(self)
                again = self.make_move(curr_player, move)
            temp = curr_player
            curr_player = wait_payer
            wait_payer = temp

        print(self)
        if self.has_won(curr_player.num):
            print("Player", curr_player, " wins with score ", self.get_score(curr_player))

        elif self.has_won(wait_payer.num):
            print("Player", wait_payer, " wins with score", self.get_score(curr_player))
        else:
            print("Tie Game")
