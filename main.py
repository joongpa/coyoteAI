from coyote import Coyote
from humanPlayer import HumanPlayer

player1 = HumanPlayer('Alice')
player2 = HumanPlayer('Bob')
player3 = HumanPlayer('Charlie')

coyote = Coyote(players=[player1, player2, player3], roundsToPlay=3)
coyote.playGame()
