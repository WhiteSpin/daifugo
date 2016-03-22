from random import shuffle
import copy

CARD_SYMBOLS = ['2','3','4','5','6','7','8','9','10','B','D','K','A']

class CardDeck(object):
    def __init__(self, standart=True):
        self.standart = standart
        self.cards = []

    def generateDeck(self):
        for j in (range(0,2) if self.standart else range(7,13)):
            for i in range(4):
                self.cards.append(j)
        
    def shuffle(self):
        shuffle(self.cards)

    def addCards(self, cards):
        for i in cards:
            self.cards.append(i)

    def removeCards(self, cards):
        for i in cards:
            self.cards.remove(i)


    def giveCardsTo(self, deck, cards):
        cards = copy.deepcopy(cards)
        deck.addCards(cards)
        self.removeCards(cards)

    def size(self):
        return len(self.cards)

    def isEmpty(self):
        return self.size() == 0

    def __repr__(self):
        self.cards.sort()
        return ' '.join([CARD_SYMBOLS[i] for i in self.cards])


class PlayerCardDeck(CardDeck):

    def getClosestMatch(deck):
        pass

class Player(object):
    def __init__(self, name):
        self.name = name
        self.deck = PlayerCardDeck()
        self.game = None
        self.rank = 0

    def makeMove(self):
        print("turn: " + self.name + " current cards: " + str(self.game.currentCards))
        print("deck: " + str(self.deck))
        move = raw_input("")
        if move == "":
            return False
        else:
            moveCards = move.split(" ")

        moveCards = [CARD_SYMBOLS.index(i) for i in moveCards]

        if(not self.playCards(moveCards)):
            print("Invalid move")
            return self.makeMove()

        return True

    def isDone(self):
        return self.rank != 0


    def playCards(self, cards):
        if(self.game.isValidMove(cards)):
            self.game.flushCurrent()
            self.deck.giveCardsTo(self.game.currentCards, cards)
            if self.deck.isEmpty():
                self.game.playerFinished(self)
            return True

        return False

class Game(object):
    def __init__(self, players):
        self.players = players
        for p in self.players:
            p.game = self

        self.reset()


    def reset(self):
        self.deck = CardDeck();
        self.currentCards = CardDeck()
        self.garbage = CardDeck()

        self.deck.generateDeck()
        self.turn = 0
        self.lastPlayer = None
        self.previousPlayer = None
        self.finished = False

        for p in self.players:
            p.rank = 0

    def flushCurrent(self):
        self.currentCards.giveCardsTo(self.garbage, self.currentCards.cards)

    def startGame(self):
        self.deck.shuffle()
        self.giveOutCards()

        while(self.finished == False):
            self.playTurn()
            print("")

        print("Game finished, will reset")

    def playerFinished(self, player):
        player.rank = max([p.rank for p in self.players]) + 1
        print("Player: " + player.name + " has finished with rank: " + str(player.rank))
        if self.allDone():
            self.finished = True
        

    def playTurn(self):
        p = self.nextPlayer()

        if self.finished:
            return

        if(self.lastPlayer):
            print("Last player: " + self.lastPlayer.name)

        if(self.lastPlayer == p or 
            (self.players[self.previosTurn()] == self.lastPlayer and self.lastPlayer != self.previousPlayer)):
            self.flushCurrent()

        if(p.makeMove()):
            self.lastPlayer = p

        if(len(self.currentCards.cards) > 0 and self.currentCards.cards[0] == 12):
            self.flushCurrent()
            return

        self.previousPlayer = p
        

    def nextPlayer(self):
        if(len(self.players) == self.turn + 1):
            self.turn = 0
        else:
            self.turn += 1

        if self.players[self.turn] == self.previousPlayer:
            self.playerFinished(self.players[self.turn])

        if self.players[self.turn].isDone(): 
            if self.allDone():
                self.finished = True
            else:
                self.nextPlayer()

        return self.players[self.turn]

    def previosTurn(self):
        turn = self.turn
        if(turn == 0):
            return len(self.players) - 1
        else:
            return turn - 1

    def allDone(self):
        for p in self.players:
            if not p.isDone():
                return False

        return True

    def isValidMove(self, cards):
        if (len(self.currentCards.cards) != len(cards) and len(self.currentCards.cards) > 0) or not allSame(cards):
            return False

        if len(self.currentCards.cards) == 0 or cards[0] > self.currentCards.cards[0]:
            print("is valid")
            return True

        return False

    def giveOutCards(self):
        while(self.deck.size() >= len(self.players)):
            for p in self.players:
                self.deck.giveCardsTo(p.deck, [self.deck.cards[0]])

def allSame(cards):
    return all(x == cards[0] for x in cards)

a = Player("A")
b = Player("B")
c = Player("C")
g = Game([a,b,c])
g.startGame()
