'''
~~~~ card.py ~~~~

Contains the Card class for the game
Functions:
    __init__ - initializes the card
    __repr__ - returns the card as a string
    compare_rank - compares the rank of the card with another card
    compare_suit - compares the suit of the card with another card
    is_same_card - checks if the card is the same as another card
    is_face_up - checks if the card is facing up
    flip - flips the card
    face_up - turns the card face up
    face_down - turns the card face down
    is_selected - checks if the card is selected
    select - selects the card
    deselect - deselects the card

Variables:
    SUITS - list of suits
    RANKS - list of ranks
    suit - suit of the card
    rank - rank of the card
    selected - if the card is selected
    facing_up - if the card is facing up
    pos - position of the card
    id - id of the card (rank + suit[0])

'''





from .misc import Pos

class Card:
    SUITS = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
    RANKS = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']

    def __init__(self, suit, rank):
        if suit not in Card.SUITS or rank not in Card.RANKS:
            raise ValueError("Invalid card suit or rank")
        self.suit = suit
        self.rank = rank
        self.selected = False
        self.facing_up = False
        self.pos = Pos()
        temp = Card.RANKS.index(self.rank) + 1
        if temp < 10:
            temp = "0" + str(temp)
        else:
            temp = str(temp)
        self.id = temp+self.suit[0]

    def __repr__(self):
        return f"{self.rank} of {self.suit}"
    
    def compare_rank(self, other):
        return self.rank == other.rank
    
    def compare_suit(self, other):
        return self.suit == other.suit
    
    def is_same_card(self, other):
        return self.compare_rank(other) and self.compare_suit(other)
    
    def is_face_up(self):
        return self.facing_up
    
    # Below 3 might be a bit redundant
    
    def flip(self):
        self.facing_up = not self.facing_up
    
    def face_up(self):
        self.facing_up = True
    
    def face_down(self):
        self.facing_up = False
        
    def is_selected(self):
        return self.selected
    
    def select(self):
        self.selected = True
    
    def deselect(self):
        self.selected = False
        

if __name__ == "__main__":
    raise Exception("This file is not meant to be ran directly!")