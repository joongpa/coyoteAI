from coyote import Coyote
from humanPlayer import HumanPlayer
from randomMoveMCTSPlayer import RandomMoveMCTSPlayer

player1 = HumanPlayer('Alice')
player2 = HumanPlayer('Bob')
player3 = RandomMoveMCTSPlayer('MCTS', sampleLimit=5000)

coyote = Coyote(players=[player1, player3])
coyote.playGame()

# coyote.updateIndices()
# print(coyote.state.playerCards, ', ', coyote.state.mysteryCard)
# coyote.state.peeks = 3*[True]
# print(coyote.state.countPossibleSums(0, 20))
# print(coyote.state.countPossibleSums(1, 20))
# print(coyote.state.countPossibleSums(2, 20))