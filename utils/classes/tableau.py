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

from .card import Card
    
class Tableau:
    
    
    def __init__(self, size = 7, game_mode = "Klondike"):
        self.RANKS = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
        self.SUITS = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
        self.tableau = [[] for _ in range(size)]
        self.size = size
        self.game_mode = game_mode # For now only Klondike
        
    
    # General
    
    def columns(self):
        return len(self.tableau)
    
    def largest_column(self):
        return max(len(column) for column in self.tableau)

    def clear(self):
        self.tableau.clear()
        self.tableau = [[] for _ in range(self.size)]
    
    def legal_selection(self, colIdx, cardIdx, allowed_cnt = None):
        if len(self.tableau[colIdx]) < cardIdx:
            return False
        if len(self.tableau[colIdx]) == cardIdx:
            return True
        if self.tableau[colIdx][cardIdx].is_face_up():
            if self.game_mode == "Klondike" or self.game_mode == "Freecell":
                prev_card = None
                if self.game_mode == "Freecell" and len(self.tableau[colIdx])-cardIdx > allowed_cnt + 1:
                    return False
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
            elif self.game_mode == "Spider":
                prev_card = None
                for i in range(cardIdx, len(self.tableau[colIdx])):
                    if prev_card == None:
                        prev_card = self.tableau[colIdx][i]
                    else:
                        if prev_card.suit != self.tableau[colIdx][i].suit:
                            return False
                        if self.RANKS.index(prev_card.rank) != self.RANKS.index(self.tableau[colIdx][i].rank) + 1:
                            return False
                        prev_card = self.tableau[colIdx][i]
            return True
        return False
        
        
    # Manipulation
    

    def deal_initial_cards(self, deck):
        if self.game_mode == "Klondike":
            for i in range(self.size):
                for j in range(i, self.size):
                    if deck.check_top_card() == None:
                        raise Exception("Card is None while populating tableau")
                    self.tableau[j].append(deck.draw_top_card())
                self.tableau[i][-1].face_up()
        elif self.game_mode == "Spider":
            for i in range(6):
                for j in range(self.size):
                    skip = False
                    if j > 3 and i > 4:
                        skip = True
                    if not skip:
                        self.tableau[j].append(deck.draw_top_card())
            for column in self.tableau:
                column[-1].face_up()
        elif self.game_mode == "Freecell":
            while len(deck.cards) > 0:
                for i in range(self.size):
                    if deck.check_top_card() != None:
                        self.tableau[i].append(deck.draw_top_card())
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
            print("Number of cards to fetch is 0")
            return None
        # Need to add a check for if the column is empty
        if len(self.tableau[column]) == 0:
            print("Column is empty")
            return None
        if number == 1:
            return [self.fetch_single_card(column)]
        cards = []
        cards = self.tableau[column][-number:]
        if self.game_mode == "Klondike":
            for i in range(1, number):
                if cards[i].suit in ['Hearts', 'Diamonds'] and cards[i-1].suit in ['Hearts', 'Diamonds']:
                    print("Red on Red sequence")
                    return None
                if cards[i].suit in ['Clubs', 'Spades'] and cards[i-1].suit in ['Clubs', 'Spades']:
                    print("Black on Black sequence")
                    return None
                if self.RANKS.index(cards[i].rank) != self.RANKS.index(cards[i-1].rank) - 1:
                    print("Rank sequence is not correct")
                    return None
        elif self.game_mode == "Spider":
            # Proper order should be ascending and same suit
            for i in range(1, number):
                if cards[i].suit != cards[i-1].suit:
                    print("Different suits")
                    return None
                if self.RANKS.index(cards[i].rank) != self.RANKS.index(cards[i-1].rank) - 1:
                    print("Rank sequence is not correct")
                    return None
        cards = [self.tableau[column].pop() for _ in range(number)]
        if len(self.tableau[column]) > 0:
            self.tableau[column][-1].face_up()
        return cards 
    
    def add_single_card(self, card, column, legal = True):
        if column < 0 or column >= self.size:
            raise ValueError("Invalid column number")
        if legal:
            if self.game_mode == "Klondike" or self.game_mode == "Freecell":
                if len(self.tableau[column]) == 0:
                    if card.rank == 'K' or self.game_mode == "Freecell":
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
                    self.tableau[column][-1].face_up()
                    return True
           
            elif self.game_mode == "Spider":
                if len(self.tableau[column]) == 0:
                    self.tableau[column].append(card)
                    self.tableau[column][-1].face_up()
                    return True
                
                # If the card is the same suit and one rank lower than the top card in the column
                # if card.suit == self.tableau[column][-1].suit:
                if self.RANKS.index(card.rank) == self.RANKS.index(self.tableau[column][-1].rank) - 1:
                    self.tableau[column].append(card)
                    self.tableau[column][-1].face_up()
                    return True
                return False
        else:
            self.tableau[column].append(card)
            return True
    
    def add_multiple_cards(self, cards, column, legal = True):
        
        if column < 0 or column >= self.size:
            raise ValueError("Invalid column number")
        if legal:
            # Check that the list of cards given is a legal sequence
            if self.game_mode == "Klondike" or self.game_mode == "Freecell":
                for i in range(1, len(cards)):
                    if cards[i].suit in ['Hearts', 'Diamonds'] and cards[i-1].suit in ['Hearts', 'Diamonds']:
                        return False
                    if cards[i].suit in ['Clubs', 'Spades'] and cards[i-1].suit in ['Clubs', 'Spades']:
                        return False
                    if self.RANKS.index(cards[i].rank) != self.RANKS.index(cards[i-1].rank) - 1:
                        return False
                    
                # Check that the top card in the column is one rank higher than the bottom card in the list
                if len(self.tableau[column]) > 0:
                    if self.RANKS.index(cards[0].rank) != self.RANKS.index(self.tableau[column][-1].rank) - 1:
                        return False
                    # color check
                    if cards[0].suit in ['Hearts', 'Diamonds'] and self.tableau[column][-1].suit in ['Hearts', 'Diamonds']:
                        return False
                    if cards[0].suit in ['Clubs', 'Spades'] and self.tableau[column][-1].suit in ['Clubs', 'Spades']:
                        return False
                else:
                    if self.game_mode == "Klondike":
                        if cards[0].rank != 'K':
                            return False
            
            elif self.game_mode == "Spider":
                for i in range(1, len(cards)):
                    # if cards[i].suit != cards[i-1].suit:
                    #     return False
                    if self.RANKS.index(cards[i].rank) != self.RANKS.index(cards[i-1].rank) - 1:
                        return False
                    
                # Check that the top card in the column is one rank higher than the bottom card in the list
                if len(self.tableau[column]) > 0:
                    if self.RANKS.index(cards[0].rank) != self.RANKS.index(self.tableau[column][-1].rank) - 1:
                        return False
                    # color check
                    # if cards[0].suit != self.tableau[column][-1].suit:
                    #     return False
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
    
    def contains_full_sequence(self):
        # Currently only used for Spider Solitaire
        for col in range(self.size):
            if len(self.tableau[col]) >= 13:
                sequence = self.tableau[col][-13:]
                if all(card.suit == sequence[0].suit for card in sequence) and all(self.RANKS.index(sequence[i].rank) == self.RANKS.index(sequence[i + 1].rank) + 1 for i in range(len(sequence) - 1)):
                    if all(card.is_face_up() for card in sequence):
                        return col
        return -1
    
    
    
    def backup(self):
        data = {}
        data["tableau"] = []
        for column in self.tableau:
            data["tableau"].append(list(card.backup() for card in column))
        data["size"] = self.size
        data["game_mode"] = self.game_mode
        return data
        
        
    def restore(self, data):
        self.clear()
        self.size = data["size"]
        self.game_mode = data["game_mode"]
        for col, column_data in enumerate(data["tableau"]):
            column = []
            for card_data in column_data:
                card = Card("", "", True)
                card.restore(card_data)
                column.append(card)
            self.tableau[col] = column
        
        
    def __repr__(self):
        return f"Tableau: {self.tableau}"
    


if __name__ == "__main__":
    raise Exception("This file is not meant to be ran directly!")