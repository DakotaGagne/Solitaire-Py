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
        self.moves = 0
        self.prevMoves = 0
        self.selected_card_location = None
        self.selected_card_overlay = None
        self.initialize_game()
        '''End of __init__()'''
        
        
    def __repr__(self):
        return f"{self.tableau}\n{self.foundation}\n{self.stock}\n"
        '''End of __repr__()'''


    def is_game_won(self):
        return all(foundation.is_complete() for foundation in self.foundation)
        '''End of is_game_won()'''
        
    def check_auto_complete(self):
        if len(self.stock.waste) > 0 or len(self.stock.stock) > 0:
            return False
        for col in self.tableau.tableau:
            if len(col) > 0:
                if col[0].rank != "K" or not col[0].is_face_up():
                    return False
        return True


    def initialize_game(self):
        self.deck.reset_deck()
        # if self._rules.always_winable:
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
    
             
    def unselect_card(self):
        # Unselects the selected card
        if self.selected_card_location != None:
            # Tableau
            if self.selected_card_location[0] == "T":
                colIdx = int(self.selected_card_location[1])
                cardIdx = int(self.selected_card_location[2:])
                if len(self.tableau.tableau[colIdx]) > cardIdx:
                    self.tableau.tableau[colIdx][cardIdx].deselect()
                if len(self.tableau.tableau[colIdx]) > cardIdx + 1:
                    for i in range(cardIdx + 1, len(self.tableau.tableau[colIdx])):
                        self.tableau.tableau[colIdx][i].deselect()
                # Need check for if the card was up in the pile, if so all below need to be deselected as well
                
            # Foundation
            elif self.selected_card_location[0] == "F":
                foundation = int(self.selected_card_location[1])
                if len(self.foundation[foundation].pile) > 0:
                    self.foundation[foundation].pile[-1].deselect()
                
            # Stock
            elif self.selected_card_location[0] == "W":
                if len(self.stock.waste) > 0:
                    self.stock.waste[-1].deselect()
            self.selected_card_location = None
        '''End of unselect_card()'''
    
        
    def move_card(self, start, end):
        # Card Can be moved to
        # Tableau from Tableau, Foundation, Waste
        # Foundation from Tableau, Waste
        
        # Start Options are Tableau, Foundation, Waste
        # End Options are Tableau, Foundation
        # Need to check if the move is legal
        # For tableau, need to consider the cards below the selected card 
        move_successful = False
        # TABLEAU
        if start[0] == "T":
            # From Tableau to Tableau
            if end[0] == "T":
                # Need check for if selected tableau is empty (would be "T0E" for example) 
                startCol = int(start[1])
                startCard = int(start[2:])
                endCol = int(end[1])
                if len(self.tableau.tableau[startCol]) == startCard + 1:
                    self.tableau.tableau[startCol][startCard].deselect()
                    if self.tableau.add_single_card(self.tableau.tableau[startCol][startCard], endCol):
                        # Successful move
                        self.tableau.tableau[startCol][-1].face_up()
                        if self.tableau.fetch_single_card(startCol) == None:
                            raise Exception("Card is None after fetching")
                        if len(self.tableau.tableau[endCol]) > 0:
                            self.tableau.tableau[endCol][-1].face_up()
                        self.moves += 1
                        move_successful = True
                    move_successful = False
                else:
                    cards = self.tableau.tableau[startCol][startCard:]
                    for card in cards:
                        card.deselect()
                    if self.tableau.add_multiple_cards(cards, endCol):
                        # Successful move
                        self.tableau.tableau[startCol][-1].face_up()
                        if self.tableau.fetch_multiple_cards(startCol, len(self.tableau.tableau[startCol]) - startCard) == None:
                            raise Exception("Card is None after fetching")
                        if len(self.tableau.tableau[endCol]) > 0:
                            self.tableau.tableau[endCol][-1].face_up()
                        self.moves += 1
                        move_successful = True
                    move_successful = False
                self.unselect_card()
            
            # From Tableau to Foundation
            elif end[0] == "F":
                startCol = int(start[1])
                startCard = int(start[2:])
                
                # Ace Check
                if end[1] == "A":
                    # Ace from tableau to foundation
                    moved = False
                    for i in range(len(self.foundation)):
                        if self.foundation[i].add_card(self.tableau.tableau[startCol][-1]):
                            self.foundation[i].pile[-1].deselect()
                            # Successful move
                            self.tableau.fetch_single_card(startCol)
                            self.moves += 1
                            moved = True
                            move_successful = True
                            break
                    if not moved:
                        print("Ace to Foundation Move Failed")
                        move_successful = False
                    self.unselect_card()
                    
                            
                if len(self.tableau.tableau[startCol]) == startCard + 1:
                    self.tableau.tableau[startCol][startCard].deselect()
                    if self.foundation[int(end[1])].add_card(self.tableau.tableau[startCol][startCard]):
                        # Successful move
                        # Remove from tableau pile
                        self.tableau.tableau[startCol].pop()
                        if len(self.tableau.tableau[startCol]) > 0:
                            self.tableau.tableau[startCol][-1].face_up()
                        self.moves += 1
                        move_successful = True
                    move_successful = False
                self.unselect_card()
            
            else:
                raise ValueError("Invalid end location")
            
        # FOUNDATION
        elif start[0] == "F":
            
            # From Foundation to Tableau
            if end[0] == "T":
                foundCol = int(start[1])
                tabCol = int(end[1])
                self.foundation[foundCol].pile[-1].deselect()
                if self.tableau.add_single_card(self.foundation[foundCol].pile[-1], tabCol):
                    # Successful move
                    # Remove from waste pile
                    self.foundation[foundCol].pile.pop()
                    self.moves += 1
                    move_successful = True
                move_successful = False
            
            # From Foundation to Foundation?
            elif end[0] == "F":
                found1Idx = int(start[1:])
                found2Idx = int(end[1:])
                self.foundation[found1Idx].pile[-1].deselect()
                if self.foundation[found2Idx].add_card(self.foundation[found1Idx].pile[-1]):
                    # Successful move
                    # Remove from foundation pile
                    self.foundation[found1Idx].pile.pop()
                    self.moves += 1
                    move_successful = True
                move_successful = False

            else:
                raise ValueError("Invalid end location")
            self.unselect_card()
        
        # WASTE
        elif start[0] == "W":
            # Can go to Tableau, Foundation
            # From Waste to Tableau
            if end[0] == "T":
                tabCol = int(end[1])
                self.stock.waste[-1].deselect()
                if self.stock.can_fetch_top_card():
                    if self.tableau.add_single_card(self.stock.waste[-1], tabCol):
                        # Successful move
                        self.tableau.tableau[tabCol][-1].face_up()
                        # Remove from waste pile
                        self.stock.fetch_top_card()
                        self.moves += 1
                        move_successful = True
                    move_successful = False
                
            
            # From Waste to Foundation
            elif end[0] == "F":
                # Ace Check
                if end[1] == "A":
                    # Ace from tableau to foundation
                    moved = False
                    for i in range(len(self.foundation)):
                        if self.foundation[i].add_card(self.stock.waste[-1]):
                            self.foundation[i].pile[-1].deselect()
                            # Successful move
                            self.stock.fetch_top_card()
                            self.moves += 1
                            moved = True
                            move_successful = True
                            break
                    if not moved:
                        print("Ace to Foundation Move Failed")
                        move_successful = False
                    
                else:
                    foundIdx = int(end[1:])
                    self.stock.waste[-1].deselect()
                    if self.stock.can_fetch_top_card():
                        if self.foundation[foundIdx].add_card(self.stock.waste[-1]):
                            # Successful move
                            # Remove from waste pile
                            self.foundation[foundIdx].pile[-1].face_up()
                            self.stock.fetch_top_card()
                            self.moves += 1
                            move_successful = True
                        move_successful = False
            else:
                raise ValueError("Invalid end location")
            self.unselect_card()
        else:
            raise ValueError("Invalid start location")
        return move_successful
        '''End of move_card()'''
    
    
    def auto_move(self):
        # Automatically moves a card to the foundation if possible
        # startLoc is the location of the card to be moved
        # Move to tableau if cant to foundation
        # Called when a double click occurs
        
        # For Tableau, need to move the entire pile if possible
        moved = False
        if self.selected_card_location[0] == "W":
            # Can go to tableau or Foundation
            self.stock.waste[-1].deselect()
            for i in range(len(self.foundation)):
                if self.foundation[i].add_card(self.stock.waste[-1]):
                    self.stock.fetch_top_card()
                    self.moves += 1
                    moved = True
                    break
                
            if not moved:
                for i in range(len(self.tableau.tableau)):
                    if self.tableau.add_single_card(self.stock.waste[-1], i):
                        self.tableau.tableau[i][-1].face_up()
                        self.stock.fetch_top_card()
                        self.moves += 1
                        moved = True
                        break
        
        elif self.selected_card_location[0] == "T":
            # Can go to tableau (minus curr col) or Foundation
            # Needs to handle multiple cards (stacks)
            colIdx = int(self.selected_card_location[1])
            cardIdx = int(self.selected_card_location[2:])
            self.tableau.tableau[colIdx][cardIdx].deselect()
            if cardIdx == len(self.tableau.tableau[colIdx]) - 1:
                # Single Card Move
                self.tableau.tableau[colIdx][cardIdx].deselect()
                for i in range(len(self.foundation)):
                        if self.foundation[i].add_card(self.tableau.tableau[colIdx][-1]):
                            self.tableau.fetch_single_card(colIdx)
                            self.moves += 1
                            moved = True
                            break
                
                if not moved:
                    for i in range(len(self.tableau.tableau)):
                        if i != colIdx and self.tableau.add_single_card(self.tableau.tableau[colIdx][-1], i):
                            self.tableau.fetch_single_card(colIdx)
                            self.moves += 1
                            moved = True
                            break
            else:
                # Multiple Card Move
                cards = self.tableau.tableau[colIdx][cardIdx:]
                for card in cards:
                    card.deselect()
                for i in range(len(self.tableau.tableau)):
                    if self.tableau.add_multiple_cards(cards, i):
                        # Successful move
                        if len(self.tableau.tableau[colIdx]) > 0:
                            self.tableau.tableau[colIdx][-1].face_up()
                        if self.tableau.fetch_multiple_cards(colIdx, len(self.tableau.tableau[colIdx]) - cardIdx) == None:
                            # raise Exception("Card is None after fetching")
                            print("ERROR!!!! Card is None after fetching!!!!")
                            print(cards)
                            print("ColIdx:", colIdx)
                            print("CardIdx:", cardIdx)
                        self.moves += 1
                        moved = True
                        break
            
            
        elif self.selected_card_location[0] == "F":
            # Can only go to tableau
            colIdx = int(self.selected_card_location[1:])
            self.foundation[colIdx].pile[-1].deselect()
            for i in range(len(self.tableau.tableau)):
                if self.tableau.add_single_card(self.foundation[colIdx].pile[-1], i):
                    self.foundation[colIdx].pop_card()
                    self.moves += 1
                    moved = True
                    break
        self.unselect_card()
        '''End of auto_move()'''
        
    
    def auto_complete(self):
        # Automatically moves all cards to the foundation if possible
        # Called when the user clicks the auto complete button\
        moved = False
        for i in range(len(self.tableau.tableau)):
            if len(self.tableau.tableau[i]) > 0:
                for j in range(len(self.foundation)):
                    if self.foundation[j].add_card(self.tableau.tableau[i][-1]):
                        self.moves += 1
                        moved = True
                        if self.tableau.fetch_single_card(i) == None:
                            print("Fetch Single Card is None")
                        break
            if moved:
                break
        if not moved:
            print("Auto Complete Failed")
        '''End of auto_complete()'''
    
    def backup(self):
        data = {}
        data["deck"] = self.deck.backup()
        data["tableau"] = self.tableau.backup()
        data["foundation"] = list(foundation.backup() for foundation in self.foundation)
        data["stock"] = self.stock.backup()
        data["moves"] = self.moves
        data["prevMoves"] = self.prevMoves
        data["selected_card_location"] = self.selected_card_location
        return data
        '''End of backup()'''
        
    def restore(self, data):
        self.deck.restore(data["deck"])
        self.tableau.restore(data["tableau"])
        for i in range(len(self.foundation)):
            self.foundation[i].restore(data["foundation"][i])
        self.stock.restore(data["stock"])
        self.moves = data["moves"]
        self.prevMoves = data["prevMoves"]
        self.selected_card_location = data["selected_card_location"]
        '''End of restore()'''
        
        


if __name__ == "__main__":
    raise Exception("This file is not meant to be ran directly!")