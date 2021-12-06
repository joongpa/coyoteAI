from coyoteState import CoyoteState
from player import Player
from typing import Tuple

class ExpectiMaxPlayer(Player):
    def __init__(self, playerName, explorationDepth, playerIndex=0, lives=3, peeks=2):
        super.__init__(playerName, playerIndex=playerIndex, lives=lives, peeks=peeks)
        self.explorationDepth = explorationDepth

    def inputMove(self, coyoteState) -> Tuple[str, bool]:
        pass

    def evaluateState(self, coyoteState: CoyoteState) -> float:
        if coyoteState.isTerminal():
            winProb = coyoteState.winLossProbability(self.playerIndex)
            if winProb > 0.9:
                return 3
            elif winProb > 0.8:
                return 2
            elif winProb > 0.5:
                return 1
            elif winProb > 0.2:
                return -2
            else:
                return -5
        currentGuess = int(coyoteState.currentGuess())
        prob = coyoteState.countPossibleSums(self.playerIndex, currentGuess)
        if self.playerIndex == coyoteState.currentPlayer():
            return 5 * (1 - prob)
        elif self.playerIndex == (coyoteState.currentPlayer() - 1) % coyoteState.numPlayers:
            return 3 * prob 
        elif self.playerIndex == (coyoteState.currentPlayer() + 1) % coyoteState.numPlayers:
            return 3 * (1 - prob)
        else:
            return 0


