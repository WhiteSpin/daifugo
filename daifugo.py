from random import shuffle

CARD_SYMBOLS = {
        0: '2',
        1: '3',
        2: '4',
        3: '5',
        4: '6',
        5: '7',
        6: '8',
        7: '9',
        8: '10',
        9: 'B',
        10: 'D',
        11: 'K',
        12: 'A'}

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


class PlayerCardDeck(CardDeck):

    def getClosestMatch(deck):
        pass

class Player(object):
    def __init__(self):
        self.deck = PlayerCardDeck()
        self.game = None

    def playCards(self, cards):
        if(self.game.isValidMove(cards)):
            self.game.currentCards.giveCardsTo(self.game.garbage, self.game.currentCards.cards)
            self.deck.giveCardsTo(self.game.currentCards, cards)

        else:
            print("Move not valid")

class Game(object):
    def __init__(self, players):
        self.players = players
        for p in self.players:
            p.game = self

        self.deck = CardDeck();
        self.currentCards = CardDeck();
        self.garbage = CardDeck();

        self.deck.generateDeck();

    def startGame(self):
        self.deck.shuffle()
        self.giveOutCards()

    def isValidMove(self, cards):
        if (len(self.currentCards.cards) != len(cards) and len(self.currentCards.cards) > 0) or not allSame(cards):
            return False

        if len(self.currentCards.cards) == 0 or cards[0] > self.currentCards.cards[0]:
            return True

        return False

    def giveOutCards(self):
        while(self.deck.size() >= len(self.players)):
            for p in self.players:
                self.deck.giveCardsTo(p.deck, [self.deck.cards[0]])

def allSame(cards):
    return all(x == cards[0] for x in cards)

a = Player()
b = Player()
c = Player()
g = Game([a,b,c])
