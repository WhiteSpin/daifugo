from random import shuffle

CARD_SYMBOLS = ['2','3','4','5','6','7','8','9','10','B','D','K','A']

class CardDeck(object):
    def __init__(self, standart=True):
        self.standart = standart
        self.cards = []

    def generateDeck(self):
        for j in (range(0,13) if self.standart else range(7,13)):
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
        deck.addCards(cards)
        self.removeCards(cards)

    def size(self):
        return len(self.cards)

    def __repr__(self):
        return ' '.join([CARD_SYMBOLS[i] for i in self.cards])


class PlayerCardDeck(CardDeck):

    def getClosestMatch(deck):
        pass

    def __repr__(self):
        return ' '.join([CARD_SYMBOLS[i] for i in self.cards])

class Player(object):
    def __init__(self, name):
        self.name = name
        self.deck = PlayerCardDeck()
        self.game = None

    def makeMove(self):
        print("turn: " + self.name + " current cards: " + str(self.game.currentCards))
        print("deck: " + str(self.deck))
        move = raw_input("")
        if move == "":
            return False
        else:
            moveCards = move.split(" ")

        moveCards = [CARD_SYMBOLS.index(i) for i in moveCards]
        print(moveCards)

        if(not self.playCards(moveCards)):
            print("Invalid move")
            self.makeMove()


    def playCards(self, cards):
        if(self.game.isValidMove(cards)):
            self.game.flushCurrent()
            self.deck.giveCardsTo(self.game.currentCards, cards)
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
        self.finished = False

    def flushCurrent(self):
        self.currentCards.giveCardsTo(self.garbage, self.currentCards.cards)

    def startGame(self):
        self.deck.shuffle()
        self.giveOutCards()

        while(self.finished == False):
            self.playTurn()

        print("Game finished, will reset")


    def playTurn(self):
        p = self.players[self.turn] 
        if(self.lastPlayer == p):
            self.flushCurrent()
        if(p.makeMove()):
            lastPlayer = p

        if(len(self.currentCards.cards) > 0 and self.currentCards.cards[0] == 12):
            self.flushCurrent()
            return

        self.nextTurn()
        

    def nextTurn(self):
        if(len(self.players) == self.turn + 1):
            self.turn = 0
        else:
            self.turn += 1

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
