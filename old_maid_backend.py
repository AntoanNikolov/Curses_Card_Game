#Antoan - Working in this file to make the game work without the visual aspects for now

class Card:
    SUITS = ('Clubs', 'Diamonds', 'Hearts', 'Spades')
    RANKS = ('narf', 'Ace', '2', '3', '4', '5', '6', '7',
             '8', '9', '10', 'Jack', 'Queen', 'King')

    def __init__(self, suit=0, rank=0):
        self.suit = suit
        self.rank = rank

    def __cmp__(self, other):
        # check the suits
        if self.suit > other.suit: return 1
        if self.suit < other.suit: return -1
        # suits are the same... check ranks
        if self.rank > other.rank: return 1
        if self.rank < other.rank: return -1
        # ranks are the same... it's a tie
        return 0

    def __str__(self):
        return '{0} of {1}'.format(Card.RANKS[self.rank],
                                   Card.SUITS[self.suit])

class Deck:
    def __init__(self):
        self.cards = []
        for suit in range(4):
            for rank in range(1, 14):
                self.cards.append(Card(suit, rank))

    def print_deck(self):
        for card in self.cards:
            print(card)

    def shuffle(self):
        import random
        num_cards = len(self.cards)
        for i in range(num_cards):
            j = random.randrange(i, num_cards)
            self.cards[i], self.cards[j] = self.cards[j], self.cards[i]
    
    def remove(self, card):
        if card in self.cards:
            self.cards.remove(card)
            return True
        else:
            return False


    def pop(self):
        return self.cards.pop()


    def is_empty(self):
        return (len(self.cards) == 0)

    def deal(self, hands, num_cards=999):
        num_hands = len(hands)
        for i in range(num_cards):
            if self.is_empty(): break   # break if out of cards
            card = self.pop()           # take the top card
            hand = hands[i % num_hands] # whose turn is next?
            hand.add(card)              # add the card to the hand


    def __str__(self):
        s = ""
        for i in range(len(self.cards)):
            s += " " * i + str(self.cards[i]) + "\n"
        return s
    
class Hand(Deck):
    def __init__(self, name=""):
       self.cards = []
       self.name = name

    def add(self,card):
        self.cards.append(card)

    def __str__(self):
        s = "Hand " + self.name
        if self.is_empty():
            s = s + " is empty\n"
        else:
            s = s + " contains\n"
        return s + Deck.__str__(self)

class CardGame:
    def __init__(self):
        self.deck = Deck()
        self.deck.shuffle()

class OldMaidGame(CardGame):
    def play(self, names):
        # remove Queen of Clubs
        self.deck.remove(Card(0,12))

        # make a hand for each player
        self.hands = []
        for name in names:
            self.hands.append(OldMaidHand(name))

        # deal the cards
        self.deck.deal(self.hands)
        print("---------- Cards have been dealt")
        self.printHands()

        # remove initial matches
        matches = self.removeAllMatches()
        print("---------- Matches discarded, play begins")
        self.printHands()

        # play until all 50 cards are matched
        turn = 0
        numHands = len(self.hands)
        while matches < 25:
            matches = matches + self.playOneTurn(turn)
            turn = (turn + 1) % numHands

        print("---------- Game is Over")
        self.printHands()

    def remove_all_matches(self):
        count = 0
        for hand in self.hands:
            count = count + hand.remove_matches()
        return count

    def play_one_turn(self, i):
        if self.hands[i].is_empty():
            return 0
        neighbor = self.find_neighbor(i)
        pickedCard = self.hands[neighbor].popCard()
        self.hands[i].add(pickedCard)
        print("Hand", self.hands[i].name, "picked", pickedCard)
        count = self.hands[i].remove_matches()
        self.hands[i].shuffle()
        return count

    def find_neighbor(self, i):
        numHands = len(self.hands)
        for next in range(1,numHands):
            neighbor = (i + next) % numHands
            if not self.hands[neighbor].is_empty():
                return neighbor
    