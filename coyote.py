from random import shuffle
from cards import Card

class Coyote:
    def __init__(self, players, roundsToPlay):
        self.players = players
        self.deck = []
        self.rounds = 0
        self.roundsToPlay = roundsToPlay

    def dealCards(self):
        cards = [c.value for c in Card]
        shuffle(cards)
        self.deck = cards[:len(self.players) + 2]

    def playRound(self):
        pass

    def calculateLossValue(self):
        sum = 0
        count = 0
        hasMystery = Card.MYSTERY in self.deck[:len(self.players) + 1]
        hasMax0 = Card.MAX0 in self.deck[:len(self.players) + 1]
        maxValue = float('-inf')
        length = len(self.players) + 1
        
        for i in range(length if not hasMystery else length + 1):
            if self.deck[count] == Card.MYSTERY or self.deck[count] == Card.MAX0:
                pass
            else:
                value = int(self.deck[i])
                sum += value
                maxValue = max(maxValue, value)
        return sum - (maxValue if hasMax0 else 0)

    def endGame(self):

        pass

    def __str__(self):
        for i in len(self.players):
            print(self.players[i], ": ", self.deck[i])