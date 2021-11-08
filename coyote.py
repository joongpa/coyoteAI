from random import shuffle
from cards import Card
from coyoteState import CoyoteState

class Coyote:
    def __init__(self, players, roundsToPlay=0):
        self.rounds = 0
        self.roundsToPlay = roundsToPlay
        self.state = CoyoteState(players, self.dealCards(len(players)))

    def dealCards(numPlayers):
        cards = [c.value for c in Card]
        shuffle(cards)
        return cards[:numPlayers + 2]

    def reset(self):
        self.state.reset(self.dealCards(self.state.numPlayers))

    def playGame(self):
        while (self.rounds < self.roundsToPlay and self.roundsToPlay != 0) or self.state.numPlayers > 1:
            self.playRound()
            print(self)
        self.endGame()

    def playRound(self):
        roundPlaying = True
        indexCounter = 0
        while(roundPlaying):
            playerIndex = indexCounter % self.state.numPlayers
            self.state = self.state.players[playerIndex].inputMove(self.state)
            if self.state.guesses[-1] == 'check':
                roundPlaying = False
                if self.state.guesses[-2] > self.calculateLossValue(self):
                    self.state.playerWon(playerIndex)
                    self.state.playerLost((indexCounter - 1) % self.state.numPlayers)
                else:
                    self.state.playerLost(playerIndex)
                    self.state.playerWon((indexCounter - 1) % self.state.numPlayers)
            indexCounter += 1
        self.rounds += 1
        self.reset()

    def calculateLossValue(self):
        sum = 0
        count = 0
        hasMystery = Card.MYSTERY in self.deck[:self.state.numPlayers + 1]
        hasMax0 = Card.MAX0 in self.deck[:self.state.numPlayers + 1]
        maxValue = float('-inf')
        length = self.state.numPlayers + 1
        
        for i in range(length if not hasMystery else length + 1):
            if self.deck[count] == Card.MYSTERY or self.deck[count] == Card.MAX0:
                pass
            else:
                value = int(self.deck[i])
                sum += value
                maxValue = max(maxValue, value)
        return sum - (maxValue if hasMax0 else 0)

    def endGame(self):
        print(self)
        pass

    def __str__(self):
        for i in len(self.players):
            print(self.players[i], ": ", self.deck[i])