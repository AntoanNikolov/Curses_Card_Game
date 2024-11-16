import random #random card selections, etc.
import time #will use this to make the game run at an enjoyable pace

class Card:
    SUITS = ['♠', '♡', '♢', '♣']
    RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']

    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def is_equal(self, other):
        return self.rank == other.rank #compare ranks for forming matches

    
    def __str__(self):
        return f"{self.rank}{self.suit}"

class Deck:
    def __init__(self):
        self.cards = []
        for suit in Card.SUITS:  #for every suit
            for rank in Card.RANKS:  #for every number value
                self.cards.append(Card(rank, suit))  #add a card to the deck with that rank and suit
    
    def shuffle_deck(self):
        random.shuffle(self.cards) #https://www.w3schools.com/python/ref_random_shuffle.asp


class Hand: #(player)
    def __init__(self, name):
        self.name = name
        self.cards = []
    
    def add_card(self, card): #add card object to the hand of the player
        self.cards.append(card)
    
    def remove_card(self,card): #remove card object from the hand of the player
        pass

    def remove_matches(self):
        pass

    def is_empty(self):
        return len(self.cards) == 0

    def __str__(self):
        print_hand = []
        for i in self.cards:
            print_hand.append(i)
        return print_hand


class Game:
    def __init__(self):
        self.players = []
        self.deck = Deck() #deck object for the game to use
    
    def start_play(self, names):
        pass

    def deal(self):
        pass

    def remove_all_matches(self): #remove matches from all players' hands at the start of the game
        for player in self.players:
            player.remove_matches()

    def check_winner(self):
        for player in self.players:
            if player.is_empty():
                print(player.name , "is out of cards and wins!")
                return True
            else:
                return False

    def play_turns(self):
        pass