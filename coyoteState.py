class CoyoteState:
    def __init__(self, players, deck):
        self.players = players
        self.numPlayers = len(players)
        self.peeks = [False] * self.numPlayers
        self.eliminatedPlayers = []
        self.deck = deck
        self.guesses = []

    def playerWon(self, index):
        self.players[index].peeks = max(self.players[index].lives, self.players[index].peeks + 1)
        self.players[index].wins += 1

    def playerLost(self, index):
        self.players[index].lives -= 1
        self.players[index].losses += 1
        if self.players[index].lives == 0:
            self.players.remove(index)
            self.eliminatedPlayers.append(self.players[index])

    def maxPossibleSum(self, playerIndex):

    def getLegalActions(self, playerIndex):
        # return current guess + 1 up to max possible value
        return ['check', 'raise'] if not self.peeks[playerIndex] else ['raise']
    
    def nextState(self, playerIndex, action):
        # apply action to state, return new state without mutation to current state
        pass

    def currentGuess(self):
        return self.guesses[-1]

    def isTerminal(self):
        return self.currentGuess() == 'check'
