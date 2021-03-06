from random import shuffle
from cards import Card
from coyoteState import CoyoteState
from random import Random
import sys

from player import Player

class Coyote:
    def __init__(self, players: list):
        self.players = list(players)
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
            self.playRound()
            print(self)
        self.endGame()
        playerDict = dict()
        winner = self.players[0]
        for player in self.eliminatedPlayers:
            playerDict[player] = (player.wins, player.losses)
        playerDict[winner] = (winner.wins, winner.losses)
        return winner, playerDict 

    def playRound(self):
        roundPlaying = True
        indexCounter = self.startingPlayer
        while(roundPlaying):
            playerIndex = indexCounter % self.state.numPlayers
            action, peek = self.players[playerIndex].inputMove(self.state)
            print(self.players[playerIndex].name(), ' chose ', action)
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
        print(f'Actual sum: {self.state.sum}')
        print(self.state.deck)
        self.resetState()

    def resetState(self):
        numPlayers = len(self.players)
        self.state = CoyoteState(numPlayers, self.dealCards(numPlayers), startingPlayer=self.startingPlayer)

    def game_summary(self):
        winner = self.players[0]
        print(f'Rounds played: {self.rounds}')
        if winner.losses != 0:
            print(f'Winner: {winner.name()}\nWin rate: {winner.wins / winner.losses}')
        else:
            print(f'Winner: {winner.name()}\nWin rate: Perfect')
        for lost_player in self.eliminatedPlayers:
            print(f'Player {lost_player.name()}\'s win rate: {lost_player.wins / lost_player.losses}')

    def endGame(self):
        print('Game over')
        self.game_summary()

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
