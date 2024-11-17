import random #random card selections, etc.
import time #will use this to make the game run at an enjoyable pace

class Card: #we will use this class to make card objects, with wich to populate the deck.
    SUITS = ['♠', '♡', '♢', '♣']
    RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']

    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def is_equal(self, other):
        return self.rank == other.rank #compare ranks for forming matches

    
    def __str__(self):
        return f"{self.rank}{self.suit}"


class Deck: #When we populate the deck with all existing cards, they will be distributed to the players
    def __init__(self):
        self.cards = []
        for suit in Card.SUITS:  #for every suit
            for rank in Card.RANKS:  #for every number value
                self.cards.append(Card(rank, suit))  #add a card to the deck with that rank and suit
    
    def shuffle_deck(self):
        random.shuffle(self.cards) #https://www.w3schools.com/python/ref_random_shuffle.asp

    def draw_card(self):
        if self.cards: #"if the deck has been populated, please take out a card from there"
            return self.cards.pop() #inspired by Jeff's code. Pop provides a convenient way of removing the last item in a list


class Hand: #(player)
    def __init__(self, name):
        self.name = name
        self.cards = []
    
    def add_card(self, card): #add card object to the hand of the player
        self.cards.append(card)
    
    def remove_card(self, index): #remove card object from the hand of the player at given index. Index is random when it is a bot's turn.
        if 0 <= index < len(self.cards):
            return self.cards.pop(index)

    def remove_matches(self): #i was getting confused a lot here, not sure if it handles iteration properly
        #sort cards to prepare for dealing with pairs
        self.cards.sort(key=lambda card: card.rank) #found this online, rarely ever used a function like this before so I needed help
        unpaired = []
        i = 0
        while i < len(self.cards): #while we have not iterated through the whole list
            if i < len(self.cards)-1: #making sure we don't get an error with the index being out of range
                if self.cards[i] == self.cards[i+1]: #checks if the cards next to each other can be paired
                    i +=2 #disregard the pair if there is one
            
            else:
                unpaired.append(self.cards[i]) #only keeping the cards that do not have pairs
                i+=1 #move ahead by one to start searching again
        random.shuffle(unpaired)
        self.cards = unpaired

    def __str__(self):
        print_hand = []
        for i in self.cards:
            print_hand.append(i)
        return print_hand


class Game:
    def __init__(self):
        self.players = []
        self.deck = Deck() #deck object for the game to use
    
    def start_play(self, names): #prepare the game and keep it running unless someone has won
        for name in names:
            self.players.append(Hand(name))
        self.deck.shuffle() #randomize the deck before we deal
        self.deal()
        self.remove_all_matches

    def deal(self):
        while self.deck.cards: #while there are still cards in the deck
            for player in self.players:
                player.add_card(self.deck.draw_card())

    def remove_all_matches(self): #remove matches from all players' hands at the start of the game
        for player in self.players:
            player.remove_matches()

    def check_winner(self):
        for player in self.players:
            if player.cards == []:
                print(player.name , "is out of cards and wins!")
                return True
            else:
                return False

    def play_turns(self): #turn logic
        pass