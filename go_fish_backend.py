import random #random card selections, etc.
import time #will use this to make the game run at an enjoyable pace


#IMPORTANT THINGS TO FIX:
#game is running but nothing is happening (occurs when the play_turns function is called)
#pop index out of range error
#find_pairs function logic is flawed

class Card: #we will use this class to make card objects, with wich to populate the deck.
    SUITS = ['♠', '♡', '♢', '♣']
    RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']

    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def __str__(self):
        return f"{self.rank}{self.suit}"
    
    ##############################################


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
        else:
            raise ValueError("No cards left in the deck to draw.")  #raise an error instead of returning None


class Hand: #(player)
    def __init__(self, name):
        self.name = name
        self.cards = []
        self.pairs = []
    
    def add_card(self, card): #add card object to the hand of the player
        self.cards.append(card)
    
    def remove_card_by_rank(self, rank): #remove card object from the hand of the player at given rank and refresh their deck. Store the card that was taken from the player in correctly_picked_cards.
        correctly_picked_cards = []
        for card in self.cards:
            if card.rank == rank: #if the card the player picked exists in the opponents hand:
                correctly_picked_cards.append(card) #grab that card from the opponent and store it in this list

        new_cards = []
        for card in self.cards: #remove the cards that have been picked from the opponent
            if card.rank != rank:
                new_cards.append(card)
        self.cards = new_cards #update the deck to take removed cards into account

        return correctly_picked_cards #we will use this variable further down below to ADD these cards to whoever's turn it was
    
    def find_pairs(self): #check the player's deck, remove, and store the pairs in self.pairs as tuples which show the suit and rank of each card in a pair.
        i = 0
        while i < len(self.cards):
            j = i+1 #the card after
            while j < len(self.cards):
                if self.cards[i].rank == self.cards[j].rank:
                    self.pairs.append((self.cards[i], self.cards[j]))
                    self.cards.pop(i)
                    self.cards.pop(j)
                    i -= 1 #the list size has been changed so we have to change the index
                    break #we need a break statement to restart the loop on the inside
                j+=1 #advance
            j+=1 #advance

    def __str__(self):
        return " ".join(str(card) for card in self.cards) #had to look this up



class Game:
    def __init__(self):
        self.players = []
        self.deck = Deck() #deck object for the game to use
    
    def start_play(self, names): #prepare the game and keep it running unless someone has won
        self.players = [Hand(name) for name in names] #for some reason this syntax is the only thing stopping an error which I do not understand. I had to resort to ChatGPT
        self.deck.shuffle_deck() #randomize the deck before we deal
        self.deal()
        for player in self.players: #remove matches from all players' hands at the start of the game
            player.find_pairs()
        
        self.play_turns()  #start the game loop

    def deal(self):
        for i in range(7): #deal 7 cards per player
            for player in self.players:
                card = self.deck.draw_card()
                player.add_card(card)

    def check_winner(self):
        for player in self.players:
            if len(player.cards) == 0:
                print(f"{player.name} has no cards left and wins!")
                return True
        
        return False

    def play_turns(self): #turn logic
        while True:
            for i, j in enumerate(self.players):

                turn = i
                
                current_player = self.players[turn]
                previous_player = self.players[(turn-1)%len(self.players)]

                if current_player.name == "You":
                    print("\n Your turn!")
                    time.sleep(1)

                    print(f"{self.players[1].name} has {len(self.players[1].cards)} cards.")
                    time.sleep(1)

                    print(f"Your hand contains: ")
                    for card in current_player.cards:
                        print(f"{card.suit} {card.rank}")
                    time.sleep(1)

                    print(f"\n You are picking from {previous_player.name}")
                    time.sleep(0.4)

                    while True: #infinite loop to keep waiting for a proper input
                        try:
                            picked_rank = input("Ask for a rank (e.g., 'A', '7'): ")
                            rank_present = False
                            for card in current_player.cards:
                                if card.rank == picked_rank:
                                    rank_present = True
                                    break
                            if rank_present:
                                break
                            else:
                                print("You must have at least one card of that rank to ask for it.")

                        except:
                            print("Invalid input. Try again.")

                    
                    correctly_picked_cards = previous_player.remove_card_by_rank(picked_rank)
                    if correctly_picked_cards: #if you have picked a card correctly
                        print(f"{previous_player.name} gives you: {', '.join(str(card) for card in correctly_picked_cards)}") #once again found this type of syntax online
                        current_player.cards.append(correctly_picked_cards)

                    else: #unsuccesful pick
                        print(f"{previous_player.name} says: 'Go Fish!'")
                        drawn_card = self.deck.draw_card()
                        if drawn_card:
                            print(f"You drew: {drawn_card}")
                            current_player.add_card(drawn_card)

                else: #opponent's turn
                    print(f"\n {current_player.name}'s turn!")
                    time.sleep(1)

                    picked_rank = random.choice(previous_player.cards).rank
                    print(f"{current_player.name} asks: 'Do you have any {picked_rank}s?'")
                    
                    correctly_picked_cards = previous_player.remove_card_by_rank(picked_rank)
                    if correctly_picked_cards:
                        print(f"You give {current_player.name}: {', '.join(str(card) for card in correctly_picked_cards)}")
                        current_player.cards.append(correctly_picked_cards)
                    
                    else:
                        print("You exclaim: 'Go Fish!'")
                        drawn_card = self.deck.draw_card()
                        if drawn_card:
                            print(f"{current_player.name} drew a card.")
                            current_player.add_card(drawn_card)

                current_player.find_pairs()
                if self.check_winner():
                    return #used to exit a function



def main():
    game = Game()
    player_names = ['You', 'Jeremy the Fish']  #Modify as needed for now
    game.start_play(player_names)

if __name__ == "__main__":
    main()