from player import Player

class HumanPlayer(Player):
    def __init__(self):
        super().__init__()

    def inputMove(self, state):
        guess = input()
        return guess, False

    def name(self):
        return 'Human'