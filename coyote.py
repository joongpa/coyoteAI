from random import shuffle
from cards import Card
from coyoteState import CoyoteState
from random import Random
import sys

from player import Player

class Coyote:
    def __init__(self, players: list):
        self.players = players
        self.eliminatedPlayers = []
        self.rounds = 0
        numPlayers = len(players)
        self.state = CoyoteState(numPlayers, self.dealCards(numPlayers))
        self.startingPlayer = 0

    def dealCards(self, numPlayers):
        cards = [c.value for c in Card]
        Random().shuffle(cards) #6 for max 0
        return cards[:numPlayers + 2]

    def playGame(self):
        self.updateIndices()
        while self.state.numPlayers > 1:
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
            action, peek = self.players[playerIndex].inputMove(self.state)
            prev_guess = self.state.currentGuess()
            self.state = self.state.nextState(playerIndex, action, peek)
            if self.state.isTerminal():
                roundPlaying = False
                if int(prev_guess) > self.state.sum:
                    # call playerWon before playerLost
                    self.playerWon(playerIndex)
                    loserIndex = (indexCounter - 1) % self.state.numPlayers
                    self.playerLost((indexCounter - 1) % self.state.numPlayers)
                    self.startingPlayer = ((loserIndex + 1) % self.state.numPlayers)
                    print('Player', playerIndex + 1, 'wins round ' + str(self.rounds + 1) + '!')
                else:
                    winnerIndex = (indexCounter - 1) % self.state.numPlayers
                    self.playerWon(winnerIndex)
                    self.playerLost(playerIndex)
                    self.startingPlayer = ((playerIndex + 1) % self.state.numPlayers)
                    print('Player', (indexCounter - 1) % self.state.numPlayers + 1, 'wins round ' + str(self.rounds + 1) + '!')
            indexCounter += 1
        self.rounds += 1
        self.resetState()

    def resetState(self):
        numPlayers = len(self.players)
        self.state = CoyoteState(numPlayers, self.dealCards(numPlayers))

    def game_summary(self):
        winner = self.players[0]
        print(f'Rounds played: {self.rounds}')
        print(f'Winner: {winner.name()}\nWin rate: {winner.wins / (1 + winner.losses)}')
        for lost_player in self.eliminatedPlayers:
            print(f'Player {lost_player.name()}\'s win rate: {lost_player.wins / (1 + lost_player.losses)}')

    def endGame(self):
        print('Game over')
        self.game_summary()
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
        lost_player = self.players[index]
        lost_player.lives -= 1
        lost_player.losses += 1
        lost_player.peeks = min(lost_player.lives, lost_player.peeks)
        if lost_player.lives == 0:
            self.players.pop(index)
            self.eliminatedPlayers.insert(0, lost_player)
            self.updateIndices()

    def updateIndices(self):
        for i in range(len(self.players)):
            player = self.players[i]
            player.playerIndex = i
