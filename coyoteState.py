import copy

class CoyoteState:
    def __init__(self, numPlayers, deck, peeks=None, guesses=None):
        # self.players = players
        self.numPlayers = numPlayers
        self.peeks = peeks if peeks else [False] * numPlayers
        self.deck = deck
        self.guesses = guesses if guesses else []


    def maxPossibleSum(self, playerIndex):
        sum = 0
        for i in range(self.numPlayers):
            if i == playerIndex:
                continue
            sum += self.deck[i]

        return sum

    def getLegalActions(self, playerIndex):
        # return current guess + 1 up to max possible value
        cur_guess = self.guesses[-1]
        actions = [i for i in range(cur_guess + 1, self.maxPossibleSum(playerIndex))]

        if not self.peeks[playerIndex]:
            actions.append('check')
        return actions
        # return ['check', 'raise'] if not self.peeks[playerIndex] else ['raise']
    
    def nextState(self, playerIndex, action, didPeek=False):
        # apply action to state, return new state without mutation to current state
        new_guesses = list(self.guesses)
        new_guesses.append(action)
        new_peeks = list(self.peeks)
        if didPeek:
            new_peeks[playerIndex] = True
        return CoyoteState(self.numPlayers, list(self.deck), new_peeks, new_guesses)

    def currentGuess(self):
        return self.guesses[-1]

    def isTerminal(self):
        return self.currentGuess() == 'check'
