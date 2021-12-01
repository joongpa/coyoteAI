from coyoteState import CoyoteState

class Node:
    def __init__(self, state: CoyoteState, parent=None):
        self.state = state
        # (action, node)
        self.children = []
        self.parent = parent

        self.isTerminal = self.state.isTerminal()
        self.visits = 0
        self.totalScore = 0
        self.isFullyExpanded = False

    def backPropagate(self, score):
        self.totalScore += score
        self.visits += 1

        if self.parent:
            self.parent.backPropagate(score)

    def __str__(self):
        string = (self.state.currentGuess() if self.state.currentGuess() else 'None') + ' {'
        for _, child in self.children:
            string += child.__str__() + ', '
        string += '}'
        return string
