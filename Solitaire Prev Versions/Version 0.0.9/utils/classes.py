import random
import pygame # type: ignore
from pygame.locals import * # type: ignore
import os
from collections import deque
from copy import deepcopy
# Maybe instead of having the image directories in the classes, have them be a key for a dictionary (stored in card class)
# In the main game file, can have the dictionary contain the directories and get referenced that way
# This way, the classes can be used for any deck, and the directories can be changed in the main game file
# Wont have to change the classes at all, just the dictionary


# Selected might not be a useful piece of data to track
# Might be best to have a highlighting feature in the pygame window that outlines the card selected




# Maybe instead of having the image directories in the classes, have them be a key for a dictionary (stored in card class)
# In the main game file, can have the dictionary contain the directories and get referenced that way
# This way, the classes can be used for any deck, and the directories can be changed in the main game file
# Wont have to change the classes at all, just the dictionary


# Selected might not be a useful piece of data to track
# Might be best to have a highlighting feature in the pygame window that outlines the card selected

class Pos:
    # helper class
    # Ex - Card.pos.x
    def __init__(self, x = None, y = None):
        self.x = x
        self.y = y
        
class Dims:
    def __init__(self, x = 0, y = 0, width = 0, height = 0):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

class Button:
    # Pygame Button
    def __init__(self, x, y, width, height, image):
        self.dims = Dims(x, y, width, height)
        self.image = image
    
    def update_dims(self, dims):
        self.dims.x = dims["x"]
        self.dims.y = dims["y"]
        self.dims.width = dims["width"]
        self.dims.height = dims["height"]
    
    def draw(self, screen):
        # change size of image
        self.image = pygame.transform.scale(self.image, (self.dims.width, self.dims.height))
        # draw image
        screen.blit(self.image, (self.dims.x, self.dims.y))
        
    def check_click(self, x, y):
        if self.dims.x <= x <= self.dims.x + self.dims.width and self.dims.y <= y <= self.dims.y + self.dims.height:
            print("UNDO CLICKED")
            return True
        return False

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

        


class Standard_Deck:
    # Designed for a standard 52 card deck, no jokers, etc
    def __init__(self):
        # Might want to add a parameter to set the type of deck
        self.SUITS = ['Clubs', 'Diamonds', 'Hearts', 'Spades']
        self.RANKS = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
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


    
    
class Tableau:
    def __init__(self, size = 7, type = "Klondike"):
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
                    if Card.RANKS.index(prev_card.rank) != Card.RANKS.index(self.tableau[colIdx][i].rank) + 1:
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
            if Card.RANKS.index(cards[i].rank) != Card.RANKS.index(cards[i-1].rank) - 1:
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
                if card.RANKS.index(card.rank) == card.RANKS.index(self.tableau[column][-1].rank) - 1:
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
                if Card.RANKS.index(cards[i].rank) != Card.RANKS.index(cards[i-1].rank) - 1:
                    print("Failed Rank Check")
                    return False
                
            # Check that the top card in the column is one rank higher than the bottom card in the list
            if len(self.tableau[column]) > 0:
                if Card.RANKS.index(cards[0].rank) != Card.RANKS.index(self.tableau[column][-1].rank) - 1:
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
        
      
      
        
class Stock:
    # First pass Complete
    # Contains the stock of cards and the waste
    # Take from stock (1 or 3), add to waste
    # If less than 3 cards in stock, move what remains (if 3 mode is true)
    # If stock is empty, move waste to stock
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
    
    
    # What other functions will I need?
    # Will need a function to check if a move is legal
    # Will need a function to check if the game is winable
    
    
    

class GameRenderer:
    def __init__(self, game, screen, images, button_images, background = (0, 100, 0)):
        self.game = game
        self.screen = screen
        self.background = background
        self.card_images = images # Dictionary of card images
        button_images = button_images
        self.dims = {
            "screen": {"width": 0, "height": 0},
            "card": {"width": 0, "height": 0},
            "tableau": {"width_proportion": 0, "height_proportion": 0, "padding": 0, "width": 0, "height": 0, "col_width": 0},
            "foundation": {"padding": 0},
            "stock": {"x": 0, "y": 0},
            "waste": {"x": 0, "y": 0},
            "undo_button": {"x": 0, "y": 0}
        }
        # Buttons
        self.undo_button = Button(0, 0, 0, 0, button_images["undo"])
        
        
        self.set_dimensions()
        
        self.states = deque()
        self.selected_card_overlay = pygame.Surface((self.dims["card"]["width"], self.dims["card"]["height"]))
        self.selected_card_overlay.set_alpha(128)  # Transparency level
        self.selected_card_overlay.fill((0, 0, 0))  # Black color
        self.selected_card_location = None
        self.test = False
        self.moves = 0
        self.prevMoves = 0
        self.store_state()
        
    def set_dimensions(self):
        self.dims["screen"]["width"], self.dims["screen"]["height"] = self.screen.get_size()
        self.dims["card"]["height"] = self.dims["screen"]["height"] * 0.15
        self.dims["card"]["width"] = self.dims["card"]["height"] * 0.7
        self.dims["tableau"]["width_ratio"] = 0.55
        self.dims["tableau"]["height_ratio"] = 0.25
        self.dims["tableau"]["width"] = self.dims["screen"]["width"] * self.dims["tableau"]["width_ratio"]
        self.dims["tableau"]["height"] = self.dims["screen"]["height"] * self.dims["tableau"]["height_ratio"]
        self.dims["tableau"]["col_width"] = self.dims["tableau"]["width"] / self.game.tableau.columns()
        self.dims["tableau"]["padding"] = 0.2
        self.dims["foundation"]["padding"] = 0.2  # Relative to foundation width
        self.dims["stock"]["x"] = self.dims["screen"]["width"] * 0.1
        self.dims["stock"]["y"] = self.dims["screen"]["height"] * 0.8
        self.dims["waste"]["x"] = self.dims["screen"]["width"] * 0.1 + self.dims["card"]["width"] * 1.5
        self.dims["waste"]["y"] = self.dims["screen"]["height"] * 0.8
        self.dims["waste"]["padding"] = self.dims["card"]["width"] * 0.5
        self.selected_card_overlay = pygame.Surface((self.dims["card"]["width"], self.dims["card"]["height"]))
        self.selected_card_overlay.set_alpha(128)  # Transparency level
        self.selected_card_overlay.fill((0, 0, 0))  # Black color
        self.dims["undo_button"]["width"] = self.dims["screen"]["width"] * 0.05
        self.dims["undo_button"]["height"] = self.dims["undo_button"]["width"]
        self.dims["undo_button"]["x"] = self.dims["undo_button"]["width"] * 0.5
        self.dims["undo_button"]["y"] = self.dims["undo_button"]["height"] * 0.5
        # Button Updates
        self.undo_button.update_dims(self.dims["undo_button"])
        

    def update(self, mouse):
        # Debuging
        if not self.test:
            self.TEST()
            self.test = True
            
        if self.moves > self.prevMoves:
            self.store_state()
            print("Stored New State")
            self.prevMoves = self.moves
            
        if self.game.is_game_won():
            print("Game Won")
            self.states.clear()
            self.game.initialize_game()
            
        
        # Mouse Click
        if mouse.x != None and mouse.y != None:
            # print(f"Mouse Clicked at: {mouse.x}, {mouse.y}")
            clicked = self.check_click(mouse.x, mouse.y)
            if clicked != None:
                self.click_handler(clicked)
            
            # Check if a card was clicked
            # Select that card (either internally, externally, or both)
        
        
        # Card Position
        self.pos_cards()
        # Draw To Screen
        self.draw()
        # Apply
        
        
    def TEST(self):
        print("Ran Test. Nothing inside tho")
        
    def pos_cards(self):
        # Tableau
        
        for col_index, column in enumerate(self.game.tableau.tableau):
            if len(column) != 0:
                chg = (self.dims["tableau"]["height"] / (self.game.tableau.largest_column() / 2))
                for row_index, card in enumerate(column):
                    card.pos.x = col_index * self.dims["tableau"]["col_width"] + (self.dims["screen"]["width"] - self.dims["tableau"]["width"]) / 2
                    card.pos.y = row_index * min(chg, self.dims["card"]["height"] * 0.5) + self.dims["card"]["height"] * 1.33
        
        # Foundation
        x_start = (self.dims["screen"]["width"] - (self.dims["card"]["width"] + self.dims["foundation"]["padding"]) * 4) - self.dims["card"]["width"]
        y_start = self.dims["card"]["height"] * self.dims["foundation"]["padding"]
        for i, foundation in enumerate(self.game.foundation):
            foundation.pos.x = x_start + i * (self.dims["card"]["width"] + self.dims["foundation"]["padding"] * self.dims["card"]["width"])
            foundation.pos.y = y_start
            if len(foundation.pile) > 0:
                for card in foundation.pile:
                    card.pos.x = foundation.pos.x
                    card.pos.y = foundation.pos.y
        
        
        self.game.stock.set_face_down("all")
        # Stock
        for card in self.game.stock.stock:
            card.pos.x = self.dims["stock"]["x"]
            card.pos.y = self.dims["stock"]["y"]
        
        # Waste
        if len(self.game.stock.waste) > 0:
            for card in self.game.stock.waste:
                card.pos.x = self.dims["waste"]["x"]
                card.pos.y = self.dims["waste"]["y"]
            
            visible = min(3, len(self.game.stock.waste), self.game.stock.waste_visible)
            for card in self.game.stock.waste: card.face_down()
            if visible < 3 and len(self.game.stock.waste) > visible:
                self.game.stock.waste[-(visible + 1)].pos.x = self.dims["waste"]["x"] + (visible) * self.dims["waste"]["padding"]
                self.game.stock.waste[-(visible + 1)].pos.y = self.dims["waste"]["y"]
            for i in range(visible):
                self.game.stock.waste[-(i + 1)].face_up()
                self.game.stock.waste[-(i + 1)].pos.x = self.dims["waste"]["x"] + (visible - i) * self.dims["waste"]["padding"]
                self.game.stock.waste[-(i + 1)].pos.y = self.dims["waste"]["y"]
            
        
        # Will need to position the cards in the tableau, foundation, stock, and waste
        # Each card is the same width and height, but the placement will be different
        # Uses the dimensions set in set_dimensions
        # Simply places all cards to a position, does not draw them
        # Ideally allows for the ability to drag a card around.
        # More features needed likely
    
    
    def draw(self):
        
        self.screen.fill(self.background)  # Fill the screen with a green color
        # Buttons
        self.undo_button.draw(self.screen)
        
        # Tableau
        for colIdx, column in enumerate(self.game.tableau.tableau):
            if len(column) == 0:
                # generate a rect the size of the column, that is a darker color than self.background
                # draw the rect
                rect_x = colIdx * self.dims["tableau"]["col_width"] + (self.dims["screen"]["width"] - self.dims["tableau"]["width"]) / 2
                rect_y = self.dims["card"]["height"] * 1.33
                pygame.draw.rect(self.screen, (int(self.background[0] * 0.5), int(self.background[1] * 0.5), int(self.background[2] * 0.5)), (rect_x, rect_y, self.dims["card"]["width"], self.dims["card"]["height"]))
            else:
                for card in column:
                    if card.is_face_up():
                        card_image = self.card_images[card.id]
                    else:
                        card_image = self.card_images['back']
                    card_image = pygame.transform.scale(card_image, (int(self.dims["card"]["width"]), int(self.dims["card"]["height"])))
                    self.screen.blit(card_image, (card.pos.x, card.pos.y))
                    if card.is_selected():
                        # Draw a transparent rectangle over card
                        # Rectangle should be dark
                        self.screen.blit(self.selected_card_overlay, (card.pos.x, card.pos.y))
                    
        # Foundation
        for foundation in self.game.foundation:
            if len(foundation.pile) == 0:
                pygame.draw.rect(self.screen, (int(self.background[0] * 0.5), int(self.background[1] * 0.5), int(self.background[2] * 0.5)), (foundation.pos.x, foundation.pos.y, self.dims["card"]["width"], self.dims["card"]["height"]))
            else: 
                if not foundation.pile[-1].is_face_up():
                    foundation.pile[-1].face_up()
                card_image = self.card_images[foundation.pile[-1].id]
                card_image = pygame.transform.scale(card_image, (int(self.dims["card"]["width"]), int(self.dims["card"]["height"])))
                self.screen.blit(card_image, (foundation.pos.x, foundation.pos.y))
                if foundation.pile[-1].is_selected():
                    # Draw a transparent rectangle over card
                    # Rectangle should be dark
                    self.screen.blit(self.selected_card_overlay, (foundation.pile[-1].pos.x, foundation.pile[-1].pos.y))
        
        # Stock
        if len(self.game.stock.stock) > 0:
            card_image = self.card_images['back']
            card_image = pygame.transform.scale(card_image, (int(self.dims["card"]["width"]), int(self.dims["card"]["height"])))
            self.screen.blit(card_image, (self.dims["stock"]["x"], self.dims["stock"]["y"]))
        else:
            pygame.draw.rect(self.screen, (int(self.background[0] * 0.5), int(self.background[1] * 0.5), int(self.background[2] * 0.5)), (self.dims["stock"]["x"], self.dims["stock"]["y"], self.dims["card"]["width"], self.dims["card"]["height"]))
        
        # Waste
        if len(self.game.stock.waste) > 0:
            visible = min(3, len(self.game.stock.waste), self.game.stock.waste_visible)
            if visible < 3 and len(self.game.stock.waste) > visible:
                card_image = self.card_images['back']
                card_image = pygame.transform.scale(card_image, (int(self.dims["card"]["width"]), int(self.dims["card"]["height"])))
                self.screen.blit(card_image, (self.dims["waste"]["x"] + self.dims["card"]["width"] * 0.5, self.dims["waste"]["y"]))
            for i in reversed(range(visible)):
                if not self.game.stock.waste[-(i + 1)].is_face_up():
                    self.game.stock.waste[-(i + 1)].face_up()
                card_image = self.card_images[self.game.stock.waste[-(i + 1)].id]
                card_image = pygame.transform.scale(card_image, (int(self.dims["card"]["width"]), int(self.dims["card"]["height"])))
                self.screen.blit(card_image, (self.game.stock.waste[-(i + 1)].pos.x, self.game.stock.waste[-(i + 1)].pos.y))
            if self.game.stock.waste[-1].is_selected():
                    # Draw a transparent rectangle over card
                    # Rectangle should be dark
                    self.screen.blit(self.selected_card_overlay, (self.game.stock.waste[-1].pos.x, self.game.stock.waste[-1].pos.y))
        else:
            pygame.draw.rect(self.screen, (int(self.background[0] * 0.5), int(self.background[1] * 0.5), int(self.background[2] * 0.5)), (self.dims["waste"]["x"] + self.dims["card"]["width"] * 0.5, self.dims["waste"]["y"], self.dims["card"]["width"], self.dims["card"]["height"]))
        

        
        pygame.display.flip()
    
        
    def unselect_card(self):
        if self.selected_card_location != None:
            # Tableau
            if self.selected_card_location[0] == "T":
                colIdx = int(self.selected_card_location[1])
                cardIdx = int(self.selected_card_location[2:])
                if len(self.game.tableau.tableau[colIdx]) > cardIdx:
                    self.game.tableau.tableau[colIdx][cardIdx].deselect()
                if len(self.game.tableau.tableau[colIdx]) > cardIdx + 1:
                    for i in range(cardIdx + 1, len(self.game.tableau.tableau[colIdx])):
                        self.game.tableau.tableau[colIdx][i].deselect()
                # Need check for if the card was up in the pile, if so all below need to be deselected as well
                
            # Foundation
            elif self.selected_card_location[0] == "F":
                foundation = int(self.selected_card_location[1])
                if len(self.game.foundation[foundation].pile) > 0:
                    self.game.foundation[foundation].pile[-1].deselect()
                
            # Stock
            elif self.selected_card_location[0] == "W":
                if len(self.game.stock.waste) > 0:
                    self.game.stock.waste[-1].deselect()
            self.selected_card_location = None
        
    def check_click(self, x, y):
        if self.undo_button.check_click(x, y):
            return "Undo"
        # Tableau Clicked
        for colIdx, column in enumerate(self.game.tableau.tableau):
            if len(column) == 0:
                rect_x = colIdx * self.dims["tableau"]["col_width"] + (self.dims["screen"]["width"] - self.dims["tableau"]["width"]) / 2
                rect_y = self.dims["card"]["height"] * 1.33
                if rect_x <= x <= rect_x + self.dims["card"]["width"] and rect_y <= y <= rect_y + self.dims["card"]["height"]:
                    print(f"Empty Tableau Clicked: {colIdx}")
                    return f"T{colIdx}E"
            for cdIdx, card in reversed(list(enumerate(column))):
                if card.pos.x <= x <= card.pos.x + self.dims["card"]["width"] and card.pos.y <= y <= card.pos.y + self.dims["card"]["height"]:
                    print(f"Tableau Clicked: {colIdx} - {card}")
                    return f"T{colIdx}{cdIdx}"
                
        # Foundation clicked
        for i, foundation in enumerate(self.game.foundation):
            if foundation.pos.x <= x <= foundation.pos.x + self.dims["card"]["width"] and foundation.pos.y <= y <= foundation.pos.y + self.dims["card"]["height"]:
                print(f"Foundation Clicked: {i}")
                return f"F{i}"
        
        # Stock Clicked
        if self.dims["stock"]["x"] <= x <= self.dims["stock"]["x"] + self.dims["card"]["width"] and self.dims["stock"]["y"] <= y <= self.dims["stock"]["y"] + self.dims["card"]["height"]:
            print("Stock Clicked")
            return "S"
        
        # Waste Clicked
        if self.dims["waste"]["x"] + self.dims["card"]["width"] * 0.5 <= x <= self.dims["waste"]["x"] + self.dims["card"]["width"] * 2.5 and self.dims["waste"]["y"] <= y <= self.dims["waste"]["y"] + self.dims["card"]["height"]:
            print("Waste Clicked")
            return "W"
        return None
            
    def click_handler(self, clicked):
        if clicked == "Undo":
            self.undo_state()
        # Tableau Clicked
        if clicked[0] == "T":
            colIdx = int(clicked[1])
            if clicked[2:] == "E":
                cardIdx = clicked[2:]
            else:
                cardIdx = int(clicked[2:])
            if self.selected_card_location == clicked:
                self.unselect_card()
            elif self.selected_card_location == None:
                if cardIdx != "E":
                    if self.game.tableau.legal_selection(colIdx, cardIdx):
                        print("Legal Selection")
                        self.game.tableau.tableau[colIdx][cardIdx].select()
                        if len(self.game.tableau.tableau[colIdx]) > cardIdx + 1:
                            for i in range(cardIdx + 1, len(self.game.tableau.tableau[colIdx])):
                                self.game.tableau.tableau[colIdx][i].select()
                        self.selected_card_location = clicked
                    else:
                        print("Illegal Selection")
                else:
                    print("Empty Column")
            elif self.selected_card_location[0] in ["F", "W", "T"]:
                self.move_card(self.selected_card_location, clicked)
            else:
                raise Exception("Selected card location is invalid")
            
        # Foundation Clicked
        elif clicked[0] == "F":
            if self.selected_card_location == clicked:
                self.unselect_card()
            elif self.selected_card_location == None:
                foundation = int(clicked[1])
                if len(self.game.foundation[foundation].pile) > 0:
                    self.game.foundation[foundation].pile[-1].select()
                    self.selected_card_location = clicked
            elif self.selected_card_location[0] in ["T", "F", "W"]:
                self.move_card(self.selected_card_location, clicked)
            else:
                raise Exception("Selected card location is invalid")
            
        # Stock Clicked
        elif clicked[0] == "S":
            self.game.stock.unselect_all("stock")
            self.game.stock.draw_card()
            self.unselect_card()
            self.moves += 1
        
        # Waste Clicked
        elif clicked[0] == "W":
            if self.selected_card_location != None or self.game.stock.waste_visible == 0:
                self.unselect_card()
            elif len(self.game.stock.waste) > 0:
                self.selected_card_location = clicked
                self.game.stock.waste[-1].select()
    
    def move_card(self, start, end):
        # Card Can be moved to
        # Tableau from Tableau, Foundation, Waste
        # Foundation from Tableau, Waste
        
        # Start Options are Tableau, Foundation, Waste
        # End Options are Tableau, Foundation
        # Need to check if the move is legal
        # For tableau, need to consider the cards below the selected card
        
        # TABLEAU
        if start[0] == "T":
            
            # From Tableau to Tableau
            if end[0] == "T":
                # Need check for if selected tableau is empty (would be "T0E" for example) 
                startCol = int(start[1])
                startCard = int(start[2:])
                endCol = int(end[1])
                if len(self.game.tableau.tableau[startCol]) == startCard + 1:
                    self.game.tableau.tableau[startCol][startCard].deselect()
                    if self.game.tableau.add_single_card(self.game.tableau.tableau[startCol][startCard], endCol):
                        # Successful move
                        print("Add Card Success")
                        self.game.tableau.tableau[startCol][-1].face_up()
                        if self.game.tableau.fetch_single_card(startCol) == None:
                            raise Exception("Card is None after fetching")
                        if len(self.game.tableau.tableau[endCol]) > 0:
                            self.game.tableau.tableau[endCol][-1].face_up()
                        self.moves += 1
                    else:
                        print("Add Card Failed")
                else:
                    print("Need to implement moving from Tableau to Tableau with multiple cards")
                    cards = self.game.tableau.tableau[startCol][startCard:]
                    for card in cards:
                        card.deselect()
                    if self.game.tableau.add_multiple_cards(cards, endCol):
                        # Successful move
                        print("Add Card Success")
                        self.game.tableau.tableau[startCol][-1].face_up()
                        if self.game.tableau.fetch_multiple_cards(startCol, len(self.game.tableau.tableau[startCol]) - startCard) == None:
                            raise Exception("Card is None after fetching")
                        if len(self.game.tableau.tableau[endCol]) > 0:
                            self.game.tableau.tableau[endCol][-1].face_up()
                        self.moves += 1
                    else:
                        print("Add Card Failed")
                self.unselect_card()
            
            # From Tableau to Foundation
            elif end[0] == "F":
                startCol = int(start[1])
                startCard = int(start[2:])
                if len(self.game.tableau.tableau[startCol]) == startCard + 1:
                    self.game.tableau.tableau[startCol][startCard].deselect()
                    if self.game.foundation[int(end[1])].add_card(self.game.tableau.tableau[startCol][startCard]):
                        # Successful move
                        # Remove from tableau pile
                        self.game.tableau.tableau[startCol].pop()
                        if len(self.game.tableau.tableau[startCol]) > 0:
                            self.game.tableau.tableau[startCol][-1].face_up()
                        self.moves += 1
                self.unselect_card()
            
            else:
                raise ValueError("Invalid end location")
            
        # FOUNDATION
        elif start[0] == "F":
            
            # From Foundation to Tableau
            if end[0] == "T":
                foundCol = int(start[1])
                tabCol = int(end[1])
                self.game.foundation[foundCol].pile[-1].deselect()
                if self.game.tableau.add_single_card(self.game.foundation[foundCol].pile[-1], tabCol):
                    # Successful move
                    # Remove from waste pile
                    self.game.foundation[foundCol].pile.pop()
                    self.moves += 1
                self.unselect_card()
            
            # From Foundation to Foundation?
            elif end[0] == "F":
                found1Idx = int(start[1:])
                found2Idx = int(end[1:])
                self.game.foundation[found1Idx].pile[-1].deselect()
                if self.game.foundation[found2Idx].add_card(self.game.foundation[found1Idx].pile[-1]):
                    # Successful move
                    # Remove from foundation pile
                    self.game.foundation[found1Idx].pile.pop()
                    self.moves += 1
                self.unselect_card()
                    
            
            else:
                raise ValueError("Invalid end location")
        # WASTE
        elif start[0] == "W":
            # Can go to Tableau, Foundation
            
            # From Waste to Tableau
            if end[0] == "T":
                tabCol = int(end[1])
                self.game.stock.waste[-1].deselect()
                if self.game.stock.can_fetch_top_card():
                    if self.game.tableau.add_single_card(self.game.stock.waste[-1], tabCol):
                        # Successful move
                        self.game.tableau.tableau[tabCol][-1].face_up()
                        # Remove from waste pile
                        self.game.stock.fetch_top_card()
                        self.moves += 1
                self.unselect_card()
            
            # From Waste to Foundation
            elif end[0] == "F":
                foundIdx = int(end[1:])
                self.game.stock.waste[-1].deselect()
                if self.game.stock.can_fetch_top_card():
                    if self.game.foundation[foundIdx].add_card(self.game.stock.waste[-1]):
                        # Successful move
                        # Remove from waste pile
                        self.game.foundation[foundIdx].pile[-1].face_up()
                        self.game.stock.fetch_top_card()
                        self.moves += 1
                self.unselect_card()
            
            else:
                raise ValueError("Invalid end location")
        else:
            raise ValueError("Invalid start location")
    
    def store_state(self):
        self.states.append(deepcopy(self.game))
        
    def undo_state(self):
        if len(self.states) > 1:
            self.states.pop()
            self.game = self.states[-1]
            self.update(Pos(None, None))
            print("Perfomed Undo")
        else:
            print("Cannot undo further")
        


    
    
    
if __name__ == "__main__":
    # Test here
    # Test Deck and Card Classes
    raise Exception("This file is not meant to be ran directly!")



        



 




        
      
      

    
    
    
