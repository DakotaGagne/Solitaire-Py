'''
~~~~ stock.py ~~~~

Contains the Stock class for the game (which also contains waste pile)

Functions:
    __init__ - initializes the stock
    __repr__ - returns the stock as a string
    set_face_down - sets the face down for all cards in the stock or waste
    unselect_all - unselects all cards in the stock or waste
    populate_stock - populates the stock with cards from the deck
    clear - clears the stock and waste pile (depending on value of 'which')
    draw_card - draws a card from the stock
    can_fetch_top_card - checks if a card can be fetched from the waste pile
    fetch_top_card - fetches the top card from the waste pile

Variables:
    stock - list of cards in the stock
    waste - list of cards in the waste pile
    draw_threes - if the stock draws three cards at a time
    waste_visible - number of visible cards in the waste pile
'''


class Stock:
    def __init__(self, draw_threes = False):
        self.stock = []
        self.waste = []
        self.draw_threes = draw_threes
        self.waste_visible = 0
        
    def __repr__(self):
        return f"Stock: {self.stock}\nWaste: {self.waste}"

    def set_face_down(self, which = "all"):
        if which == "stock" or which == "all":
            if len(self.stock) > 0:
                for card in self.stock:
                    card.face_down()
        if which == "waste" or which == "all":  
            if len(self.waste) > 0: 
                for card in self.waste:
                    card.face_down()
        return True
    
    def unselect_all(self, which = "all"):
        if which == "stock" or which == "all":
            if len(self.stock) > 0:
                for card in self.stock:
                    card.deselect()
        if which == "waste" or which == "all":
            if len(self.waste) > 0:
                for card in self.waste:
                    card.deselect()
                
    def populate_stock(self, deck):
        while len(deck.cards) > 0:
            card = deck.draw_top_card()
            if card == None:
                raise Exception("Card is None while populating stock")
            self.stock.append(card)
        return deck

    def clear(self):
        self.stock = []
        self.waste = []
        self.waste_visible = 0

    def draw_card(self):
        if len(self.stock) > 0:
            if self.draw_threes:
                cards = [self.stock.pop() for _ in range(3)]
                self.waste.extend(cards)
            else:
                card = self.stock.pop()
                self.waste.append(card)
            self.set_face_down()
            if not self.draw_threes and len(self.stock) > 0:
                self.waste[-1].face_up()
                self.waste_visible += 1
                if self.waste_visible > 3:
                    self.waste_visible = 3
            else:
                for card in self.waste[-3:]:
                    card.face_up()
        else:
            self.set_face_down("all")
            while len(self.waste) > 0:
                self.stock.append(self.waste.pop())
            self.waste.clear()
            
    def can_fetch_top_card(self):
        return len(self.waste) > 0 and self.waste_visible > 0
        
    def fetch_top_card(self):
        if len(self.waste) > 0 and self.waste_visible > 0:
            card = self.waste.pop()
            self.waste_visible -= 1
            print("Waste Visible: ", self.waste_visible)
            if len(self.waste) > 0 and self.waste_visible > 0:
                self.waste[-1].face_up()
            return card
        else:
            return None
        
        
if __name__ == "__main__":
    raise Exception("This file is not meant to be ran directly!")