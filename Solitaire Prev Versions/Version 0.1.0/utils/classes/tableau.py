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
    type - type of tableau (Klondike)

Currently Only able to handle Klondike Solitaire
Will be adding more generalization in the future

'''
    
class Tableau:
    
    
    def __init__(self, size = 7, type = "Klondike"):
        self.RANKS = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
        self.SUITS = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
        self.tableau = [[] for _ in range(size)]
        self.size = size
        self.type = type # For now only Klondike
        
    
    # General
    
    def columns(self):
        return len(self.tableau)
    
    def largest_column(self):
        return max(len(column) for column in self.tableau)

    def clear(self):
        self.tableau = [[] for _ in range(self.size)]
    
    def legal_selection(self, colIdx, cardIdx):
        if len(self.tableau[colIdx]) < cardIdx:
            print("Card Index out of range")
            return False
        if len(self.tableau[colIdx]) == cardIdx:
            return True
        if self.tableau[colIdx][cardIdx].is_face_up():
            prev_card = None
            for i in range(cardIdx, len(self.tableau[colIdx])):
                if prev_card == None:
                    prev_card = self.tableau[colIdx][i]
                else:
                    if prev_card.suit in ['Hearts', 'Diamonds'] and self.tableau[colIdx][i].suit in ['Hearts', 'Diamonds']:
                        return False
                    if prev_card.suit in ['Clubs', 'Spades'] and self.tableau[colIdx][i].suit in ['Clubs', 'Spades']:
                        return False
                    if self.RANKS.index(prev_card.rank) != self.RANKS.index(self.tableau[colIdx][i].rank) + 1:
                        return False
                    prev_card = self.tableau[colIdx][i]
            return True
        return False
        
        
    # Manipulation
    

    def deal_initial_cards(self, deck):
        if self.type == "Klondike":
            for i in range(self.size):
                for j in range(i, self.size):
                    if deck.check_top_card() == None:
                        raise Exception("Card is None while populating tableau")
                    self.tableau[j].append(deck.draw_top_card())
                self.tableau[i][-1].face_up()
        return deck

    def fetch_single_card(self, column):
        if column < 0 or column >= self.size:
            raise ValueError("Invalid column number")
        if len(self.tableau[column]) > 0:
            card = self.tableau[column].pop()
            if len(self.tableau[column]) > 0:
                self.tableau[column][-1].face_up()
            return card
        else:
            return None
        
    def fetch_multiple_cards(self, column, number):
        if column < 0 or column >= self.size:
            raise ValueError("Invalid column number")
        if number < 0 or number > len(self.tableau[column]):
            raise ValueError("Invalid number of cards to fetch")
        if number == 0:
            return None
        # Need to add a check for if the column is empty
        if len(self.tableau[column]) == 0:
            return None
        if number == 1:
            return [self.fetch_single_card(column)]
        cards = []
        cards = self.tableau[column][-number:]
        for i in range(1, number):
            if cards[i].suit in ['Hearts', 'Diamonds'] and cards[i-1].suit in ['Hearts', 'Diamonds']:
                return None
            if cards[i].suit in ['Clubs', 'Spades'] and cards[i-1].suit in ['Clubs', 'Spades']:
                return None
            if self.RANKS.index(cards[i].rank) != self.RANKS.index(cards[i-1].rank) - 1:
                return None
        cards = [self.tableau[column].pop() for _ in range(number)]
        if len(self.tableau[column]) > 0:
            self.tableau[column][-1].face_up()
        return cards 
    
    def add_single_card(self, card, column, legal = True):
        if column < 0 or column >= self.size:
            raise ValueError("Invalid column number")
        if legal:
            if self.type == "Klondike":
                if len(self.tableau[column]) == 0:
                    if card.rank == 'K':
                        self.tableau[column].append(card)
                        self.tableau[column][-1].face_up()
                        return True
                    else:
                        return False
                # If the card is the opposite color and one rank lower than the top card in the column
                if card.suit == 'Hearts' or card.suit == 'Diamonds':
                    if self.tableau[column][-1].suit == 'Hearts' or self.tableau[column][-1].suit == 'Diamonds':
                        return False
                else:
                    if self.tableau[column][-1].suit == 'Clubs' or self.tableau[column][-1].suit == 'Spades':
                        return False
                # If the card is one rank lower than the top card in the column
                if self.RANKS.index(card.rank) == self.RANKS.index(self.tableau[column][-1].rank) - 1:
                    self.tableau[column].append(card)
                    print("Added Card to Column")
                    self.tableau[column][-1].face_up()
                    return True
                        
        else:
            self.tableau[column].append(card)
            return True
    
    def add_multiple_cards(self, cards, column, legal = True):
        # NOTE: I am concerned about pulling and pushing order of cards. There is a chance the code reverses the order of the cards
        # make sure to use the add_single_card one at a time, after checking legality
        if column < 0 or column >= self.size:
            raise ValueError("Invalid column number")
        if legal:
            # Check that the list of cards given is a legal sequence
            for i in range(1, len(cards)):
                if cards[i].suit in ['Hearts', 'Diamonds'] and cards[i-1].suit in ['Hearts', 'Diamonds']:
                    print("Failed Suit Check")
                    return False
                if cards[i].suit in ['Clubs', 'Spades'] and cards[i-1].suit in ['Clubs', 'Spades']:
                    print("Failed Suit Check")
                    return False
                if self.RANKS.index(cards[i].rank) != self.RANKS.index(cards[i-1].rank) - 1:
                    print("Failed Rank Check")
                    return False
                
            # Check that the top card in the column is one rank higher than the bottom card in the list
            if len(self.tableau[column]) > 0:
                if self.RANKS.index(cards[0].rank) != self.RANKS.index(self.tableau[column][-1].rank) - 1:
                    print("Failed Top Card Check")
                    return False
                # color check
                if cards[0].suit in ['Hearts', 'Diamonds'] and self.tableau[column][-1].suit in ['Hearts', 'Diamonds']:
                    print("color check 1 failed")
                    return False
                if cards[0].suit in ['Clubs', 'Spades'] and self.tableau[column][-1].suit in ['Clubs', 'Spades']:
                    print("color check 2 failed")
                    return False
            else:
                if cards[0].rank != 'K':
                    print("Failed King Card Check")
                    return False
            # If all checks pass, add the cards to the column
            for card in cards:
                self.tableau[column].append(card)
                self.tableau[column][-1].face_up()
            return True
        else:
            for card in cards:
                self.tableau[column].append(card)
                self.tableau[column][-1].face_up()
            return True
        
    def __repr__(self):
        return f"Tableau: {self.tableau}"
    


if __name__ == "__main__":
    raise Exception("This file is not meant to be ran directly!")