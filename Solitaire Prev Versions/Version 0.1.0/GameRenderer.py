'''
~~~~ gameRenderer.py ~~~~

Contains the GameRenderer class for the game
Interacts with main.py to render the game
Will be used to handle all game types ("Klondike", "Spider", etc)
Will not be used to handle menu or non game rendering

Functions:
    __init__ - initializes the game renderer
    set_dimensions - sets the dimensions of the game
    update - updates the game
    pos_cards - positions the cards
    draw - draws the game
    unselect_card - unselects a card
    check_click - checks if a click is valid
    click_handler - handles a click
    move_card - moves a card

Variables:
    game - the game being rendered
    screen - the screen being rendered to
    background - the background color of the screen
    card_images - dictionary of card images
    button_images - dictionary of button images
    dims - dictionary of dimensions
    undo_button - button to undo a move
    states - deque of game states
    selected_card_overlay - overlay for selected card
    selected_card_location - location of selected card
    moves - number of moves
    prevMoves - previous number of moves
    

'''

import pygame # type: ignore
from pygame.locals import * # type: ignore
from collections import deque
from copy import deepcopy
from utils.classes.misc import Pos, Dims
from utils.classes.ui import Button
from utils.classes.klondike import Klondike


class GameRenderer:
    def __init__(self, game_mode, screen, images, button_images, background = (0, 100, 0)):
        self.game_mode = game_mode
        if game_mode == "Klondike":
            game = Klondike()
        else:
            raise ValueError("Invalid game mode")
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
            "undo_button": {"x": 0, "y": 0, "width": 0, "height": 0}
        }
        # Buttons
        self.undo_button = Button(button_images["undo"], Dims())
        
        
        self.set_dimensions()
        
        self.states = deque()
        self.selected_card_overlay = pygame.Surface((self.dims["card"]["width"], self.dims["card"]["height"]))
        self.selected_card_overlay.set_alpha(128)  # Transparency level
        self.selected_card_overlay.fill((0, 0, 0))  # Black color
        self.selected_card_location = None
        self.moves = 0
        self.prevMoves = 0
        self.store_state()
        
    def set_dimensions(self):
        # Sets all the dimensions to the default settings
        # Based on screen size to be scalable
        
        # Dims Updates
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
        
        '''End of set_dimensions()'''
        

    def update(self, mouse):
        
        # Store State Check
        if self.moves > self.prevMoves:
            self.store_state()
            print("Stored New State")
            self.prevMoves = self.moves
        
        # Game Win Check
        if self.game.is_game_won():
            print("Game Won")
            self.states.clear()
            self.game.initialize_game()
        
        # Game Loss Check (To be implemented...)
            
        
        # Mouse Click Check
        if mouse.x != None and mouse.y != None:
            clicked = self.check_click(mouse.x, mouse.y)
            if clicked != None:
                self.click_handler(clicked)
            
            # Check if a card was clicked
            # Select that card (either internally, externally, or both)
        
        
        # Card Positioning
        self.pos_cards()
        
        # Draw To Screen
        self.draw()
        '''End of update()'''
    
    
    def pos_cards(self):
        # Sets the pos of each card depending on its location
        
        # Tableau Cards
        for col_index, column in enumerate(self.game.tableau.tableau):
            if len(column) != 0:
                chg = (self.dims["tableau"]["height"] / (self.game.tableau.largest_column() / 2))
                for row_index, card in enumerate(column):
                    card.pos.x = col_index * self.dims["tableau"]["col_width"] + (self.dims["screen"]["width"] - self.dims["tableau"]["width"]) / 2
                    card.pos.y = row_index * min(chg, self.dims["card"]["height"] * 0.5) + self.dims["card"]["height"] * 1.33
        
        # Foundation Cards
        x_start = (self.dims["screen"]["width"] - (self.dims["card"]["width"] + self.dims["foundation"]["padding"]) * 4) - self.dims["card"]["width"]
        y_start = self.dims["card"]["height"] * self.dims["foundation"]["padding"]
        for i, foundation in enumerate(self.game.foundation):
            foundation.pos.x = x_start + i * (self.dims["card"]["width"] + self.dims["foundation"]["padding"] * self.dims["card"]["width"])
            foundation.pos.y = y_start
            if len(foundation.pile) > 0:
                for card in foundation.pile:
                    card.pos.x = foundation.pos.x
                    card.pos.y = foundation.pos.y
        
        
        
        # Stock Cards
        self.game.stock.set_face_down("all")
        for card in self.game.stock.stock:
            card.pos.x = self.dims["stock"]["x"]
            card.pos.y = self.dims["stock"]["y"]
        
        # Waste Cards
        if len(self.game.stock.waste) > 0:
            for card in self.game.stock.waste:
                card.pos.x = self.dims["waste"]["x"]
                card.pos.y = self.dims["waste"]["y"]
            
            # Waste pile should have at most 3 cards face up
            # If a card is taken from waste pile, then there should be 2 cards face up, etc
            # If fewer than 3 cards in waste pile, then that many should be face up
            
            
            visible = min(3, len(self.game.stock.waste), self.game.stock.waste_visible) # Number of visible cards in waste pile
            
            for card in self.game.stock.waste: card.face_down() # Face down all cards in waste pile
            
            if visible < 3 and len(self.game.stock.waste) > visible:
                self.game.stock.waste[-(visible + 1)].pos.x = self.dims["waste"]["x"] + (visible) * self.dims["waste"]["padding"]
                self.game.stock.waste[-(visible + 1)].pos.y = self.dims["waste"]["y"]
            for i in range(visible):
                self.game.stock.waste[-(i + 1)].face_up()
                self.game.stock.waste[-(i + 1)].pos.x = self.dims["waste"]["x"] + (visible - i) * self.dims["waste"]["padding"]
                self.game.stock.waste[-(i + 1)].pos.y = self.dims["waste"]["y"]
        '''End of pos_cards()'''
    
    
    def draw(self):
        # Draws all cards to the screen based on their positions
        
        # Background
        self.screen.fill(self.background)
        
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

        # Update Screen
        pygame.display.flip()
        '''End of draw()'''
    
        
    def unselect_card(self):
        # Unselects the selected card
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
        '''End of unselect_card()'''
        
        
        
    def check_click(self, x, y):
        # Checks if a click is valid
        # Returns the location of the click
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
        '''End of check_click()'''
            
    def click_handler(self, clicked):
        # Handles a click
        # Clicked is the location of the current click
        # References self.selected_card_location as the previous click
        
        # Undo Clicked
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
        '''End of click_handler()'''
        
        
        
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
        '''End of move_card()'''
    
    def store_state(self):
        self.states.append(deepcopy(self.game))
        '''End of store_state()'''
        
    def undo_state(self):
        if len(self.states) > 1:
            self.states.pop()
            self.game = self.states[-1]
            self.update(Pos(None, None))
            print("Perfomed Undo")
        else:
            print("Cannot undo further")
        '''End of undo_state()'''
        


    
    
    
if __name__ == "__main__":
    raise Exception("This file is not meant to be ran directly!")


