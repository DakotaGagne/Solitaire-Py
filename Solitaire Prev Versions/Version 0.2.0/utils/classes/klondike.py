'''
~~~~ klondike.py ~~~~

Contains the Klondike class for the game (acts as a wrapper to use the other 
                                            classes in tandem and operate 
                                                based on the rules of klondike)

Functions:
    __init__ - initializes the game
    __repr__ - returns the game as a string
    is_game_won - checks if the game is won
    initialize_game - initializes the game
    
Variables:
    deck - deck of cards
    tableau - tableau of cards
    foundation - list of foundation piles
    stock - stock of cards
    game_rules - rules of the game (will be added later) (will be a dict containing the rules that can be modified (draw three, can undo, always winable, etc)) 

'''

from .deck import Standard_Deck
from .tableau import Tableau
from .foundation import Foundation
from .stock import Stock


class Klondike:
    # Will want to add a win check
    # Will want to add a legal move check
    # Will want to add a winable check for init
    def __init__(self):
        self.deck = Standard_Deck()
        self.tableau = Tableau()
        self.foundation = [Foundation() for _ in range(4)]
        self.stock = Stock()
        self.initialize_game()
        
    def __repr__(self):
        return f"{self.tableau}\n{self.foundation}\n{self.stock}\n"


    def is_game_won(self):
        return all(foundation.is_complete() for foundation in self.foundation)


    def initialize_game(self):
        self.deck.reset_deck()
        # if self.game_rules.always_winable:
        #    self.deck = self.gen_winable_game()
        # else:
        #   self.deck.shuffle()
        self.deck.shuffle()
        self.tableau.clear()
        self.stock.clear()
        for f in self.foundation:
            f.clear()
        self.deck = self.tableau.deal_initial_cards(self.deck)
        self.deck = self.stock.populate_stock(self.deck)
        if self.deck.length() > 0:
            raise Exception("Deck not empty after initialization")
        
    def backup(self):
        print("Backup")
        data = {}
        # Tableau
        tab = []
        for col in self.tableau.tableau:
            tab.append([card for card in col])
        data['tableau'] = tab
        # Foundation
        fnd = []
        for f in self.foundation:
            fnd.append([card for card in f.pile])
        data['foundation'] = fnd
        # Stock
        data['stock'] = [card for card in self.stock.stock]
        # Waste
        data['waste'] = [card for card in self.stock.waste]
        return data
        
    def restore(self, data):
        print("Restore")
        # Tableau
        for i, col in enumerate(data['tableau']):
            self.tableau.tableau[i] = [card for card in col]
        # Foundation
        for i, f in enumerate(data['foundation']):
            self.foundation[i].pile = [card for card in f]
        # Stock
        self.stock.stock = [card for card in data['stock']]
        # Waste
        self.stock.waste = [card for card in data['waste']]
        


if __name__ == "__main__":
    raise Exception("This file is not meant to be ran directly!")