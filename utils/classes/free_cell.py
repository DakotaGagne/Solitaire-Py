'''
~~~~ tableau.py ~~~~

Contains the Tableau class for the game

Functions:
    __init__ - initializes the tableau
    columns - returns the number of columns in the tableau
    largest_column - returns the largest column in the tableau
    clear - clears the tableau
    legal_selection - checks if a selection is legal
    deal_initial_cards - deals the initial cards to the tableau
    fetch_single_card - fetches a single card from a column
    fetch_multiple_cards - fetches multiple cards from a column
    add_single_card - adds a single card to a column
    add_multiple_cards - adds multiple cards to a column
    __repr__ - returns the tableau as a string
    
Variables:
    RANKS - list of ranks
    SUITS - list of suits
    tableau - list of columns
    size - size of the tableau
    game_mode - game_mode of tableau (Klondike)

More Generalized to be able to handle different game modes

'''

from .misc import Pos
from .card import Card

class Free_cell:
    def __init__(self):
        self.card = None
        self.cellCnt = 4
        self.pos = Pos()
        
    
    def __ref__(self):
        return f"{self.card}"
    
    def add_card(self, card):
        if self.card == None:
            self.card = card
            return True
        return False

    def fetch_card(self, cell):
        card = self.card
        self.card = None
        return card
    
    def clear(self):
        self.card = None
    
    def is_empty(self):
        return self.card == None

    def backup(self):
        data = {}
        data["card"] = None if self.card == None else self.card.backup()
        data["pos"] = [self.pos.x, self.pos.y]
        return data

    def restore(self, data):
        self.card = None if data["card"] == None else Card("", "", True)
        if self.card != None:
            self.card.restore(data["card"])
        self.pos = Pos(data["pos"][0], data["pos"][1])