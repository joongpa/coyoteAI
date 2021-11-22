from coyote import Coyote
from humanPlayer import HumanPlayer
from randomMoveMCTSPlayer import RandomMoveMCTSPlayer

player1 = HumanPlayer('Alice')
player2 = HumanPlayer('Bob')
player3 = RandomMoveMCTSPlayer('Mat MCTS', sampleLimit=10000)

coyote = Coyote(players=[player1, player2, player3])
coyote.playGame()
