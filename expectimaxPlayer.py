from player import Player
from typing import Tuple

class ExpectiMaxPlayer(Player):
    def __init__(self, playerName, explorationDepth, playerIndex=0, lives=3, peeks=2):
        super.__init__(playerName, playerIndex=playerIndex, lives=lives, peeks=peeks)
        self.explorationDepth = explorationDepth

    def inputMove(self, coyoteState) -> Tuple[str, bool]:
        pass

    def evaluateState(self, coyoteState) -> float:
        pass