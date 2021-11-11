from random import shuffle
from cards import Card
from coyoteState import CoyoteState
import sys

class Coyote:
    def __init__(self, players, roundsToPlay=0):
        self.players = players
        self.eliminatedPlayers = []
        self.rounds = 0
        self.roundsToPlay = roundsToPlay
        self.state = CoyoteState(players, self.dealCards(len(players)))

    def dealCards(self, numPlayers):
        cards = [c.value for c in Card]
        shuffle(cards)
        return cards[:numPlayers + 2]

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
            action, peek = self.players[playerIndex].inputMove(self.state)
            prev_guess = self.state.currentGuess()
            self.state = self.state.nextState(playerIndex, action, peek)
            if self.state.isTerminal():
                roundPlaying = False
                if prev_guess > self.calculateLossValue():
                    self.playerWon(playerIndex)
                    self.playerLost((indexCounter - 1) % self.state.numPlayers)
                else:
                    self.playerLost(playerIndex)
                    self.playerWon((indexCounter - 1) % self.state.numPlayers)
            indexCounter += 1
        self.rounds += 1
        self.resetState()

    def resetState(self):
        self.state = CoyoteState(len(self.players), self.dealCards(len(self.players)))

    def calculateLossValue(self):
        sum = 0
        count = 0
        hasMystery = Card.MYSTERY in self.state.deck[:self.state.numPlayers + 1]
        hasMax0 = Card.MAX0 in self.state.deck[:self.state.numPlayers + 1]
        maxValue = float('-inf')
        length = self.state.numPlayers + 1
        
        for i in range(length if not hasMystery else length + 1):
            if self.state.deck[count] == Card.MYSTERY or self.state.deck[count] == Card.MAX0:
                pass
            else:
                value = int(self.state.deck[i])
                sum += value
                maxValue = max(maxValue, value)
        return sum - (maxValue if hasMax0 else 0)

    def endGame(self):
        print(self)
        sys.exit()

    def __str__(self):
        for i in range(self.state.numPlayers):
            print(self.players[i], ": ", self.state.deck[i])

    def playerWon(self, index):
        self.players[index].peeks = max(self.players[index].lives, self.players[index].peeks + 1)
        self.players[index].wins += 1

    def playerLost(self, index):
        self.players[index].lives -= 1
        self.players[index].losses += 1
        if self.players[index].lives == 0:
            self.players.remove(index)
            self.eliminatedPlayers.append(self.players[index])