class PlayerAgent:
    def __init__(self, lives=3, peeks=2):
        self.lives = lives
        self.peeks = peeks
        self.wins = 0
        self.losses = 0

    def getAction(coyoteState):
        pass

    def evaluateState(coyoteState):
        pass

    def __str__(self):
        print(self.name(), ": ", self.wins, " wins, ", self.losses)

    
