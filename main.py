from coyote import Coyote
from humanPlayer import HumanPlayer

player1 = HumanPlayer(0, 'Alice')
player2 = HumanPlayer(1, 'Bob')
player3 = HumanPlayer(2, 'Charlie')

coyote = Coyote(players=[player1, player2, player3], roundsToPlay=3)
coyote.playGame()
