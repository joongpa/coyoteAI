from coyoteState import CoyoteState
from player import Player
from typing import Tuple
import random
import math
from node import Node
from typing import Tuple

class SimpleProbPlayer(Player):
    def __init__(self, playerName, calloutProb=0.10, playerIndex=0, lives=3, peeks=2):
        super().__init__(playerName, playerIndex, lives, peeks)
        self.calloutProb = calloutProb

    def inputMove(self, coyoteState: CoyoteState) -> Tuple[str, bool]:
        doPeek = False
        canCheck = True
        if self.peeks > 0 and not coyoteState.peeks[self.playerIndex]:
            doPeek = True
            self.peeks -= 1
            coyoteState = coyoteState.peekNextState(self.playerIndex)
            canCheck = False
        curGuess = coyoteState.currentGuess()
        if curGuess:
            prob = coyoteState.countPossibleSums(self.playerIndex, int(curGuess))
            if prob < self.calloutProb and canCheck:
                return 'check', doPeek
            else:
                return str(int(curGuess) + 1), doPeek
        else:
            return -15, doPeek