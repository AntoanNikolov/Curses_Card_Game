import random #random card selections, etc.
import time #will use this to make the game run at an enjoyable pace

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
        #remove one queen
        for card in self.cards:
            if card.rank == 'Q' and card.suit == '♣':
                self.cards.remove(card)
                break

    def shuffle_deck(self):
        random.shuffle(self.cards) #https://www.w3schools.com/python/ref_random_shuffle.asp

    def draw_card(self):
        if self.cards: #"if the deck has been populated, please take out a card from there"
            return self.cards.pop() #inspired by Jeff's code. Pop provides a convenient way of removing the last item in a list
        else:
            return None


class Hand: #(player)
    def __init__(self, name):
        self.name = name
        self.cards = []
    
    def add_card(self, card): #add card object to the hand of the player
        self.cards.append(card)
    
    def remove_card(self, index): #remove card object from the hand of the player at given index. Index is random when it is a bot's turn.
        if 0 <= index < len(self.cards):
            return self.cards.pop(index)
        else:
            return None

    def remove_matches(self):
        #sort cards to prepare for dealing with pairs
        self.cards.sort(key=lambda x: x.rank) #found this online, rarely ever used a function like this before so I needed help
        unpaired = []
        i = 0
        while i < len(self.cards)-1: #while we have not iterated through the whole list
            if self.cards[i].rank == self.cards[i+1].rank: #checks if the cards next to each other can be paired
                i +=2 #disregard the pair if there is one
            
            else:
                unpaired.append(self.cards[i]) #only keeping the cards that do not have pairs
                i+=1 #move ahead by one to start searching again
        if i == len(self.cards) - 1:
            unpaired.append(self.cards[i])
        random.shuffle(unpaired)
        self.cards = unpaired

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
            player.remove_matches()
        
        self.play_turns()  #start the game loop

    def deal(self):
        while self.deck.cards: #while there are still cards in the deck
            for player in self.players:
                player.add_card(self.deck.draw_card())

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
                    for k in self.players:
                        print(f"{k.name}: {len(k.cards)} cards.")
                    time.sleep(1)
                    print(f"\n You are picking from {previous_player.name}")
                    time.sleep(0.4)
                    picked_index = int(input(f"\n Please pick a card from {previous_player.name} (type 1-{len(previous_player.cards)}): ")) -1
                    time.sleep(0.4)
                    
                    picked_card = previous_player.cards.pop(picked_index)
                    current_player.cards.append(picked_card)
                    print(f"\n You picked {picked_card.suit} {picked_card.rank} from {previous_player.name}")
                    self.check_winner()

                else:
                    print(f"\n {current_player.name}'s turn!")
                    time.sleep(1)

                    picked_card = random.choice(previous_player.cards)
                    current_player.cards.append(picked_card)
                    print(f"{current_player.name} picked a card from {previous_player.name}")
                    turn+=1
                    self.check_winner()

                current_player.remove_matches()
                if self.check_winner():
                    return #used to exit a function



def main():
    game = Game()
    player_names = ['You', 'Bot 1', 'Bot 2']  #Modify as needed for now
    game.start_play(player_names)

if __name__ == "__main__":
    main()