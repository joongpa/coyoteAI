from player import Player
from coyoteState import CoyoteState
from typing import Tuple

class HumanPlayer(Player):
    def __init__(self, playerIndex, playerName, lives=3, peeks=2):
        super().__init__(playerIndex, playerName, lives, peeks)

    def inputMove(self, state: CoyoteState) -> Tuple[str, bool]:
        if not state.peeks[self.playerIndex]:
            peek = input('Peek? [y/n]\n')
            if peek == 'y':
                if self.peeks == 0:
                    print('No remaining peeks')
                    didPeek = False
                else:
                    self.peeks -= 1
                    didPeek = True
                    state = state.peekNextState(self.playerIndex)
            else:
                didPeek = False
        else:
            didPeek = True

        actions = state.getLegalActions(self.playerIndex)
        guess = input('Player ' + str(self.playerIndex + 1) + ', choose: ' + actions.__str__() + '\n')    
            
        if guess not in actions:
            print('Error: Enter a valid action')
            return self.inputMove(state)
        else:
            return guess, didPeek
