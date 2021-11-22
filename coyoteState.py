from cards import Card
import random
import itertools

class CoyoteState:
    def __init__(self, numPlayers: int, deck: list, peeks: list = None, guesses: list = None):
        self.numPlayers = numPlayers
        self.peeks = peeks if peeks else [False] * numPlayers
        self.deck = deck
        self.playerCards = deck[:self.numPlayers + 1]
        self.mysteryCard = deck[self.numPlayers + 1] if Card.MYSTERY.value in self.playerCards else None
        self.guesses = guesses if guesses else []
        self.currentPlayerCanCheck = True
        self.sum = CoyoteState.calculateSum(playerCards=self.playerCards, mysteryCard=self.mysteryCard)

    def currentPlayer(self):
        return (len(self.guesses) % self.numPlayers)

    @staticmethod
    def calculateSum(playerCards: list, mysteryCard=None):
        sum = 0
        if mysteryCard:
            hasMax0 = Card.MAX0.value in playerCards or Card.MAX0.value == mysteryCard
        else:
            hasMax0 = Card.MAX0.value in playerCards
        maxValue = float('-inf')

        for i in range(len(playerCards)):
            if playerCards[i] == Card.MYSTERY.value:
                if mysteryCard != Card.MAX0.value:
                    sum += int(mysteryCard)
            elif playerCards[i] == Card.MAX0.value:
                pass
            else:
                value = int(playerCards[i])
                sum += value
                maxValue = max(maxValue, value)
        return sum - (maxValue if hasMax0 else 0)

    def maxPossibleSum(self, playerIndex: int) -> int:
        sum = 0
        first, second, third = self._maxCardsPossible(playerIndex, self.peeks[playerIndex])
        length = self.numPlayers + 1 if self.peeks[playerIndex] else self.numPlayers
        for i in range(length):
            if i == playerIndex:
                sum += int(first)
                # print(f'{playerIndex + 1}\'s highest possible card: ', first)
            elif self.deck[i] == Card.MYSTERY.value:
                sum += int(second)
                # print('Highest possible mystery card: ', second)
            elif self.deck[i] == Card.MAX0.value:
                sum -= 20
            else:
                sum += int(self.deck[i])
        if not self.peeks[playerIndex]:
            if not self.mysteryCard:
                sum += int(second)
            else:
                sum += int(third)
        # print(f'{playerIndex + 1}\'s highest possible sum: {sum}')
        return sum

    def _maxCardsPossible(self, playerIndex, peeked=False):
        endIndex = self.numPlayers + 1 if peeked else self.numPlayers
        cards = [c.value for c in Card if
                 c.value not in self.playerCards[:endIndex] or c.value == self.playerCards[playerIndex]]
        return cards[-1], cards[-2], cards[-3]

    def _currentMaxCard(self, playerIndex: int, peeked=False) -> int:
        endIndex = self.numPlayers + 1 if peeked else self.numPlayers
        cards = [int(c) for c in self.playerCards[:endIndex] if
                 c != Card.MYSTERY.value and c != Card.MAX0.value and c != self.playerCards[playerIndex]]
        return max(cards)

    def getLegalActions(self, playerIndex: int) -> list:
        # return current guess + 1 up to max possible value
        if not self.guesses:
            first = True
            lower_guess = -15
            upper_guess = self.maxPossibleSum(playerIndex)
        else:
            cur_guess = int(self.guesses[-1])
            first = False
            lower_guess = cur_guess + 1
            upper_guess = min(lower_guess + 20, self.maxPossibleSum(playerIndex))
        actions = [str(i) for i in range(lower_guess, max(lower_guess + 1, upper_guess + 1))]

        if self.currentPlayerCanCheck and not first:
            actions.append('check')
        return actions

    def peekNextState(self, playerIndex):
        new_guesses = list(self.guesses)
        new_peeks = list(self.peeks)
        new_peeks[playerIndex] = True
        newState = CoyoteState(self.numPlayers, list(self.deck), new_peeks, new_guesses)
        newState.currentPlayerCanCheck = False
        return newState

    def nextState(self, playerIndex, action, didPeek=False):
        # apply action to state, return new state without mutation to current state
        new_guesses = list(self.guesses)
        new_guesses.append(action)
        new_peeks = list(self.peeks)
        if didPeek:
            new_peeks[playerIndex] = True
        return CoyoteState(self.numPlayers, self.deck, new_peeks, new_guesses)

    def currentGuess(self):
        try:
            return self.guesses[-1]
        except IndexError:
            return None

    def countPossibleSums(self, playerIndex, value):
        deckCopy = list(self.playerCards)
        endIndex = self.numPlayers + 1 if self.peeks[playerIndex] else self.numPlayers
        outsideCards = [c.value for c in Card if
                 (c.value not in self.playerCards[:endIndex] 
              or c.value == self.playerCards[playerIndex])
              and c.value != Card.MYSTERY.value]
        if not self.peeks[playerIndex]:
            del deckCopy[self.numPlayers]
        del deckCopy[playerIndex]
        if self.mysteryCard and Card.MYSTERY.value in deckCopy:
            deckCopy.remove(Card.MYSTERY.value)
        unknowns = len(self.playerCards) - len(deckCopy)
        perms = list(itertools.permutations(outsideCards, unknowns))
        count = 0
        length = len(perms)
        for perm in perms:
            newList = deckCopy + list(perm)
            sum = self.calculateSum(newList)
            if value <= sum:
                count += 1
        return count / length
        

    def winLossProbability(self, playerIndex):
        guessPlayer = (self.currentPlayer() - 2) % self.numPlayers
        checkPlayer = (self.currentPlayer() - 1) % self.numPlayers
        lastGuess = int(self.guesses[-2])
        if playerIndex != guessPlayer and playerIndex != checkPlayer:
            return 0
        elif playerIndex == guessPlayer:
            prob = self.countPossibleSums(playerIndex, lastGuess) 
            return prob
        elif playerIndex == checkPlayer:
            prob = self.countPossibleSums(playerIndex, lastGuess) 
            return 1 - prob

    def isTerminal(self):
        return self.currentGuess() == 'check'
