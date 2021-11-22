from typing import Tuple

class Player:
    def __init__(self, playerName, playerIndex=0, lives=3, peeks=2):
        self.lives = lives
        self.peeks = min(lives, peeks)
        self.wins = 0
        self.losses = 0
        self.playerIndex = playerIndex
        self.playerName = playerName

    def inputMove(self, coyoteState) -> Tuple[str, bool]:
        pass

    def name(self):
        return self.playerName

    def __str__(self):
        return f'{self.playerIndex + 1}: {self.playerName}: {self.lives} lives, {self.peeks} peeks, ' \
               f'{self.wins} wins, {self.losses} losses'
