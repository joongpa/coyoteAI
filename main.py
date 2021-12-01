from coyote import Coyote
from humanPlayer import HumanPlayer
from randomMoveMCTSPlayer import RandomMoveMCTSPlayer
from simpleProbPlayer import SimpleProbPlayer

player1 = HumanPlayer('Alice')
player2 = HumanPlayer('Bob')
player3 = RandomMoveMCTSPlayer('MCTS1', sampleLimit=1000)
player4 = RandomMoveMCTSPlayer('MCTS2', sampleLimit=1000)
player5 = RandomMoveMCTSPlayer('MCTS3', sampleLimit=1000)
player6 = SimpleProbPlayer('Simple', calloutProb=0.1)

coyote = Coyote(players=[player6, player3, player4])
coyote.playGame()

# coyote.updateIndices()
# print(coyote.state.playerCards, ', ', coyote.state.mysteryCard)
# coyote.state.peeks = 3*[True]
# print(coyote.state.countPossibleSums(0, 20))
# print(coyote.state.countPossibleSums(1, 20))
# print(coyote.state.countPossibleSums(2, 20))