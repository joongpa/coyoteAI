class CoyoteState:
    def __init__(self, players, deck):
        self.players = players
        self.eliminatedPlayers = []
        self.numPlayers = len(players)
        self.deck = deck
        self.guesses = []

    def reset(self, deck):
        self.guesses = []
        self.deck = deck

    def playerWon(self, index):
        self.players[index].peeks = max(self.players[index].lives, self.players[index].peeks + 1)
        self.players[index].wins += 1

    def playerLost(self, index):
        self.players[index].lives -= 1
        self.players[index].losses += 1
        if self.players[index].lives == 0:
            self.players.remove(index)
            self.eliminatedPlayers.append(self.players[index])

    def addGuess(self, guess):
        self.guesses.append(guess)