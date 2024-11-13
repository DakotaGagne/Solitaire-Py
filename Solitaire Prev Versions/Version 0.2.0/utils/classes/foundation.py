'''
~~~~ foundation.py ~~~~

Contains the Foundation class for the game

Functions:
    __init__ - initializes the foundation
    __repr__ - returns the foundation as a string
    can_add - checks if a card can be added to the foundation
    clear - clears the foundation
    add_card - adds a card to the foundation
    contains_card - checks if the foundation contains a card
    is_complete - checks if the foundation is complete
    is_empty - checks if the foundation is empty
    reset_foundation - resets the foundation

Variables:
    RANKS - list of ranks
    SUITS - list of suits
    pile - list of cards in the foundation
    suit - suit of the foundation
    direction - direction of the foundation (ascending or descending)
    type - type of foundation (Klondike)
    pos - position of the foundation

Note: Foundation only contains one pile of cards (unlike tableau)

'''


from .misc import Pos

class Foundation:
    # A single foundation pile
    def __init__(self, direction = "ascending", type = "Klondike"):
        self.RANKS = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
        self.SUITS = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
        self.pile = []
        self.suit = None
        self.direction = direction
        self.type = type
        self.pos = Pos()
        
    def __repr__(self):
        return f"Foundation: {self.pile}"

    def can_add(self, card):
        if self.direction == "ascending":
            if self.suit is None:
                return card.rank == 'A'
            return self.suit == card.suit and self.RANKS.index(card.rank) == self.RANKS.index(self.pile[-1].rank) + 1
        if self.direction == "descending":
            if self.suit is None:
                return card.rank == 'K'
            return self.suit == card.suit and self.RANKS.index(card.rank) == self.RANKS.index(self.pile[-1].rank) - 1
        
    def clear(self):
        self.pile = []
    
    def add_card(self, card, legal = True):
        # Adds a card to the foundation only if it is legal to do so
        # If legal is False, will add the card regardless of legality
        # Returns True if the card was added, False if it was not
        if self.suit != None and len(self.pile) == 0:
            self.suit = None
        
        if self.can_add(card) or not legal:
            if len(self.pile) == 0:
                self.suit = card.suit
            if len(self.pile) > 0:
                self.pile[-1].face_down()
            self.pile.append(card)
            self.pile[-1].face_up()
            return True
        return False

    def pop_card(self):
        # Pops the top card from the foundation
        # Returns the card that was popped
        if len(self.pile) == 0:
            return None
        card = self.pile.pop()
        if len(self.pile) > 0:
            self.pile[-1].face_up()
        return card
            
    def contains_card(self, card):
        for c in self.pile:
            if c.compare_rank(card) and c.compare_suit(card):
                return True
        return False
            
    def is_complete(self):
        if self.type == "Klondike":
            return len(self.pile) == 13
        # May need to add other completions for other game types
        
    def is_empty(self):
        return len(self.pile) == 0 and self.suit == None
    
    def reset_foundation(self):
        self.pile.clear()
        self.suit = None
        return True


if __name__ == "__main__":
    raise Exception("This file is not meant to be ran directly!")