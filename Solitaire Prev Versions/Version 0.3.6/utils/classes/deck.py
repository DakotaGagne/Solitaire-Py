'''
~~~~ deck.py ~~~~
Currently contains the Standard_Deck class for the game
Will have more deck types as needed in this file



Standard_Deck:
    Functions:
        __init__ - initializes the deck
        length - returns the length of the deck
        shuffle - shuffles the deck
        sort - sorts the deck
        is_legal - checks if the deck is legal
        is_empty - checks if the deck is empty
        check_top_card - checks the top card of the deck
        draw_top_card - draws the top card of the deck
        draw_random_card - draws a random card from the deck
        draw_specific_card - draws a specific card from the deck
        add_card - adds a card to the deck
        reset_deck - resets the deck
    Variables:
        SUITS - list of suits
        RANKS - list of ranks
        cards - list of cards in the deck


'''




from .card import Card
import random

class Standard_Deck:
    # Designed for a standard 52 card deck, no jokers, etc
    RANKS = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
    SUITS = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
    def __init__(self):
        # Might want to add a parameter to set the type of deck
        self.cards = list(Card(suit, rank) for suit in self.SUITS for rank in self.RANKS)

    # General
    
    def length(self):
        return len(self.cards)

    def shuffle(self):
        random.shuffle(self.cards)
    
    def sort(self, ascending = True, suit_first = True):
        if suit_first:
            # Sort by suit, then rank, according to self.RANKS and self.SUITS
            self.cards.sort(key = lambda x: (x.id[2], x.id[0:2]), reverse= not ascending)
        else:
            # Sort by rank, then suit, according to self.RANKS and self.SUITS
            self.cards.sort(key = lambda x: (x.id[0:2], x.id[2]), reverse= not ascending)
            
        
        return True
        # Might need more methods. Unsure atm

    def is_legal(self):
        legal = True
        for i in range(len(self.cards)-1):
            for j in range(i + 1, len(self.cards)):
                if self.cards[i].compare_rank(self.cards[j]) and self.cards[i].compare_suit(self.cards[j]):
                    legal = False
        return legal
    
    
    def is_empty(self):
        return len(self.cards) == 0
    
    # Individual
    def check_top_card(self):
        return self.cards[-1] if len(self.cards) > 0 else None
    
    def draw_top_card(self):
        return self.cards.pop() if len(self.cards) > 0 else None
    
    def draw_random_card(self):
        if not self.cards:
            return None
        return self.cards.pop(random.randint(0, len(self.cards) - 1)) if len(self.cards) > 0 else None
    
    def draw_specific_card(self, rank, suit):
        if not self.cards:
            return None
        for i in range(len(self.cards)):
            if self.cards[i].rank == rank and self.cards[i].suit == suit:
                return self.cards.pop(i)

    def add_card(self, card, legal_required = True):
        if legal_required:
            self.cards.append(card)
            if self.is_legal():
                return True
            else:
                self.cards.pop()
                return False
        else:
            self.cards.append(card)
            return True
    
    def reset_deck(self, shuffle = True):
        self.cards.clear()
        self.cards = list(Card(suit, rank) for suit in self.SUITS for rank in self.RANKS)
        if shuffle:
            self.shuffle()
        return True
    
    def backup(self):
        data = {}
        data["cards"] = list(card.backup() for card in self.cards)
        return data
    
    def restore(self, data):
        self.cards.clear()
        for card_data in data["cards"]:
            card = Card("", "", True)
            card.restore(card_data)
            self.cards.append(card)



class Spider_Deck:
    # Designed for a standard 52 card deck, no jokers, etc
    RANKS = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
    SUITS = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
    def __init__(self, suitCnt = 1):
        # Might want to add a parameter to set the type of deck
        self.suitCnt = suitCnt
        if suitCnt == 4:
            self.cards = list(Card(suit, rank) for suit in self.SUITS for rank in self.RANKS) * 2
        elif suitCnt == 2:
            self.cards = list(Card(suit, rank) for suit in [self.SUITS[0], self.SUITS[3]] for rank in self.RANKS) * 4
        elif suitCnt == 1:
            self.cards = list(Card(suit, rank) for suit in [self.SUITS[3]] for rank in self.RANKS) * 8

    # General
    
    def length(self):
        return len(self.cards)

    def shuffle(self):
        random.shuffle(self.cards)
    
    def sort(self, ascending = True, suit_first = True):
        # Might be broken by multiples of the same suit
        # Not likely to be used anyway so worth ignoring for now
        if suit_first:
            # Sort by suit, then rank, according to self.RANKS and self.SUITS
            self.cards.sort(key = lambda x: (x.id[2], x.id[0:2]), reverse= not ascending)
        else:
            # Sort by rank, then suit, according to self.RANKS and self.SUITS
            self.cards.sort(key = lambda x: (x.id[0:2], x.id[2]), reverse= not ascending)
            
        
        return True
        # Might need more methods. Unsure atm

    def is_legal(self):
        legal = True
        if len(self.cards) != 104:
                legal = False
        if self.suitCnt == 4:
            for i in range(len(self.cards)-1):
                for j in range(i + 1, len(self.cards)):
                    if self.cards[i].compare_rank(self.cards[j]) and self.cards[i].compare_suit(self.cards[j]):
                        legal = False
        elif self.suitCnt == 2:
            suits_used = []
            for i in range(len(self.cards)-1):
                for j in range(i + 1, len(self.cards)):
                    if self.cards[i].rank not in suits_used:
                        suits_used.append(self.cards[i].rank)
                        if len(suits_used) > 2:
                            legal = False
                    if self.cards[i].compare_rank(self.cards[j]):
                        legal = False
        else:
            suits_used = []
            for i in range(len(self.cards)-1):
                for j in range(i + 1, len(self.cards)):
                    if self.cards[i].rank not in suits_used:
                        suits_used.append(self.cards[i].rank)
                        if len(suits_used) > 1:
                            legal = False
                    if self.cards[i].compare_rank(self.cards[j]):
                        legal = False
        return legal
    
    
    def is_empty(self):
        return len(self.cards) == 0
    
    # Individual
    def check_top_card(self):
        return self.cards[-1] if len(self.cards) > 0 else None
    
    def draw_top_card(self):
        return self.cards.pop() if len(self.cards) > 0 else None
    
    def draw_random_card(self):
        if not self.cards:
            return None
        return self.cards.pop(random.randint(0, len(self.cards) - 1)) if len(self.cards) > 0 else None
    
    def draw_specific_card(self, rank, suit):
        if not self.cards:
            return None
        for i in range(len(self.cards)):
            if self.cards[i].rank == rank and self.cards[i].suit == suit:
                return self.cards.pop(i)

    def add_card(self, card, legal_required = True):
        if legal_required:
            self.cards.append(card)
            if self.is_legal():
                return True
            else:
                self.cards.pop()
                return False
        else:
            self.cards.append(card)
            return True
    
    def reset_deck(self, shuffle = True):
        self.cards.clear()
        if self.suitCnt == 4:
            self.cards = list(Card(suit, rank) for suit in self.SUITS for rank in self.RANKS) * 2
        elif self.suitCnt == 2:
            self.cards = list(Card(suit, rank) for suit in [self.SUITS[0], self.SUITS[3]] for rank in self.RANKS) * 4
        elif self.suitCnt == 1:
            self.cards = list(Card(suit, rank) for suit in [self.SUITS[3]] for rank in self.RANKS) * 8
        if shuffle:
            self.shuffle()
        return True
    
    def backup(self):
        data = {}
        data["cards"] = list(card.backup() for card in self.cards)
        return data
    
    def restore(self, data):
        self.cards.clear()
        for card_data in data["cards"]:
            card = Card("", "", True)
            card.restore(card_data)
            self.cards.append(card)




if __name__ == "__main__":
    raise Exception("This file is not meant to be ran directly!")