from player import Player

class HumanPlayer(Player):
    def inputMove(self, state):
        guess = input()
        state.addGuess(guess)

    def name(self):
        return 'Human'