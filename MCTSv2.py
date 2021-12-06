from coyoteState import CoyoteState
from player import Player
from typing import Tuple
import random
import math
from node import Node
from typing import Tuple


class MCTS_player_v2(Player):
    def __init__(self, playerName, sampleLimit=1000, playerIndex=0, lives=3, peeks=2):
        super().__init__(playerName, playerIndex, lives, peeks)
        self.sampleLimit = sampleLimit

    def inputMove(self, coyoteState: CoyoteState) -> Tuple[str, bool]:
        peek = False
        root = Node(coyoteState)
        if self.peeks > 0 and not coyoteState.peeks[self.playerIndex]:
            if coyoteState.currentGuess() and coyoteState.countPossibleSums(self.playerIndex,
                                                                            int(coyoteState.currentGuess())) > 0.15:
                peek = True
                self.peeks -= 1
                root = Node(coyoteState.peekNextState(self.playerIndex))
        for _ in range(self.sampleLimit):
            node = self.select(root)
            score = self.rollout(node.state)
            node.backPropagate(score)

        action, node = self.bestMove(root, 0)
        return action, peek

    def select(self, node: Node):
        while not node.isTerminal:
            if node.isFullyExpanded:
                _, node = self.bestMove(node, 4)
            else:
                if node.visits == 0:
                    return node
                else:
                    return self.expand(node)
        return node

    def expand(self, node: Node):
        playerIndex = self.playerIndex
        actions = node.state.getLegalActions(playerIndex)
        for action in actions:
            state = node.state.nextState(playerIndex, action)
            newNode = Node(state, node)

            node.children.append((action, newNode))

            if len(actions) == len(node.children):
                node.isFullyExpanded = True

        return node.children[0][1]

    def bestMove(self, node: Node, explConst):
        maxScore = float('-inf')
        bestMoves = []

        for action, child in node.children:
            if node.state.currentPlayer() == self.playerIndex: 
                playerCoeff = 1
            elif node.state.currentPlayer() == (self.playerIndex + 1) % node.state.numPlayers: 
                playerCoeff = -0.8
            else:
                playerCoeff = -0.3

            try:
                move_score = playerCoeff * child.totalScore / child.visits + explConst * math.sqrt(
                    math.log(node.visits) / child.visits)
            except:
                move_score = float('inf')
            if move_score > maxScore:
                maxScore = move_score
                bestMoves = [(action, child)]
            elif move_score == maxScore:
                bestMoves.append((action, child))
        return random.choice(bestMoves)

    def rollout(self, state: CoyoteState):
        playerIndex = self.playerIndex
        while not state.isTerminal():
            legalActions = state.getLegalActions(playerIndex)
            # state = state.nextState(playerIndex, random.choice(legalActions))
            weights = []
            for action in legalActions:
                if action != 'check':
                    # square the difference when the value is lower than expected, else 1
                    weight = (int(action) - state.sum)**2 if int(action) < state.sum else 1 # not sure about the state.sum here
                    weights.append(weight)
                else:
                    # the other way around for check
                    weight = (int(state.currentGuess()) - state.sum)**2 if int(state.currentGuess()) > state.sum else 1
                    weights.append(weight)

            if state.currentPlayer() == playerIndex or not state.currentGuess():
                state = state.nextState(playerIndex, random.choices(legalActions, weights)[0])
            else:
                if state.countPossibleSums(playerIndex, int(state.currentGuess())) < 0.1:
                    action = 'check'
                else:
                    action = random.choices(legalActions, weights)[0]
                state = state.nextState(playerIndex, action)
        val = self.terminalStateValue(state)
        return val

    def terminalStateValue(self, coyoteState: CoyoteState) -> int:
        # winProb = coyoteState.winLossProbability(self.playerIndex)
        # return winProb - (1 - winProb)
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
