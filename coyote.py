from random import shuffle
from cards import Card
from coyoteState import CoyoteState
from random import Random
import sys

from player import Player

class Coyote:
    def __init__(self, players:list[Player], roundsToPlay=0):
        self.players = players
        self.eliminatedPlayers = []
        self.rounds = 0
        self.roundsToPlay = roundsToPlay
        numPlayers = len(players)
        self.state = CoyoteState(numPlayers, self.dealCards(numPlayers))
        # self.sum = self.calculateLossValue()
        self.startingPlayer = 0

    def dealCards(self, numPlayers):
        cards = [c.value for c in Card]
        Random().shuffle(cards) #6 for max 0
        return cards[:numPlayers + 2]

    def playGame(self):
        while (self.rounds < self.roundsToPlay and self.roundsToPlay != 0) or self.state.numPlayers > 1:
            print(f'Actual sum: {self.state.sum}')
            self.playRound()
            print(self)
        self.endGame()

    def playRound(self):
        print(self.state.deck)
        roundPlaying = True
        indexCounter = self.startingPlayer
        while(roundPlaying):
            playerIndex = indexCounter % self.state.numPlayers
            if playerIndex in self.eliminatedPlayers:
                indexCounter += 1
                continue
            action, peek = self.players[playerIndex].inputMove(self.state)
            prev_guess = self.state.currentGuess()
            self.state = self.state.nextState(playerIndex, action, peek)
            if self.state.isTerminal():
                roundPlaying = False
                if int(prev_guess) > self.state.sum:
                    self.playerWon(playerIndex)
                    loserIndex = (indexCounter - 1) % self.state.numPlayers
                    self.playerLost((indexCounter - 1) % self.state.numPlayers)
                    self.startingPlayer = loserIndex + 1
                    print('Player', playerIndex + 1, 'wins round ' + str(self.rounds + 1) + '!')
                else:
                    self.playerLost(playerIndex)
                    self.startingPlayer = playerIndex + 1
                    self.playerWon((indexCounter - 1) % self.state.numPlayers)
                    print('Player', (indexCounter - 1) % self.state.numPlayers + 1, 'wins round ' + str(self.rounds + 1) + '!')
            indexCounter += 1
        self.rounds += 1
        self.resetState()

    def resetState(self):
        numPlayers = len(self.players) - len(self.eliminatedPlayers)
        self.state = CoyoteState(numPlayers, self.dealCards(numPlayers))
        # self.sum = self.calculateLossValue()

    # def calculateLossValue(self):
    #     sum = 0
    #     if self.state.mysteryCard:
    #         hasMax0 = Card.MAX0.value in self.state.deck[:self.state.numPlayers + 1]
    #     else:
    #         hasMax0 = Card.MAX0.value in self.state.playerCards or Card.MAX0.value == self.state.centerCard
    #     maxValue = float('-inf')

    #     for i in range(len(self.state.playerCards)):
    #         if self.state.playerCards[i] == Card.MYSTERY.value or self.state.playerCards[i] == Card.MAX0.value:
    #             sum += self.state.mysteryCard
    #         else:
    #             value = int(self.state.deck[i])
    #             sum += value
    #             maxValue = max(maxValue, value)
    #     return sum - (maxValue if hasMax0 else 0)

    def endGame(self):
        print('Game over')
        sys.exit()

    def __str__(self):
        s: str = ''
        for i in range(len(self.players)):
            if i not in self.eliminatedPlayers:
                s += f'{self.players[i]}\n'
        return s

    def playerWon(self, index):
        self.players[index].peeks = min(self.players[index].lives, self.players[index].peeks + 1)
        self.players[index].wins += 1

    def playerLost(self, index):
        self.players[index].lives -= 1
        self.players[index].losses += 1
        if self.players[index].lives == 0:
            self.eliminatedPlayers.append(index)