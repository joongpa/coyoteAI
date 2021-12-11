from coyote import Coyote
from humanPlayer import HumanPlayer
from randomMoveMCTSPlayer import RandomMoveMCTSPlayer
from simpleProbPlayer import SimpleProbPlayer
from MCTSv2 import MCTS_player_v2
from random import shuffle
from collections import Counter

player1 = HumanPlayer('Alice', lives=2)
player2 = HumanPlayer('Bob')
player3 = RandomMoveMCTSPlayer('MCTSv1', sampleLimit=1000, lives=2)
player3_2 = RandomMoveMCTSPlayer('MCTSv1_2', sampleLimit=1200, lives=2)
player4 = MCTS_player_v2('MCTSv2', sampleLimit=800, lives=2)
player6 = SimpleProbPlayer('Simple1', calloutProb=0.1, lives=2)
player7 = SimpleProbPlayer('Simple2', calloutProb=0.1, lives=2)
player8 = SimpleProbPlayer('Simple3', calloutProb=0.1, lives=2)
player9 = SimpleProbPlayer('Simple4', calloutProb=0.1, lives=2)

# players=[player3, player6, player7, player8, player9]
players=[player3, player6]
playerDict = dict()
playerWins = Counter()
for i in range(1):
    coyote = Coyote(players=players)
    print('Game', i + 1)
    winner, playerDictTemp = coyote.playGame()
    playerWins[winner] += 1
    shuffle(players)

    for player in players:
        player.lives = 2
        player.peeks = 2
print()
for player, wins in playerWins.items():
    print(player.name(), 'won', wins, 'times')
for player in players:
    print(player.name(), ':', player.wins, 'wins,', player.losses, 'losses')
# coyote.updateIndices()
# print(coyote.state.playerCards, ', ', coyote.state.mysteryCard)
# coyote.state.peeks = 3*[True]
# print(coyote.state.countPossibleSums(0, 20))
# print(coyote.state.countPossibleSums(1, 20))
# print(coyote.state.countPossibleSums(2, 20))