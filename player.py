class Player:
    def __init__(self, playerIndex, playerName, lives=3, peeks=2):
        self.lives = lives
        self.peeks = peeks
        self.wins = 0
        self.losses = 0
        self.playerIndex = playerIndex
        self.playerName = playerName

    def inputMove(coyoteState):
        pass

    def name(self):
        pass

    def __str__(self):
        return f'{self.playerIndex + 1}: {self.playerName}: {self.lives} lives, {self.peeks} peeks, {self.wins} wins, {self.losses} losses'
