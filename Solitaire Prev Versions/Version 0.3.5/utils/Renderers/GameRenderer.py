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
from ..classes.misc import Pos, Dims
from ..classes.ui import ButtonImg, Text
from ..classes.klondike import Klondike
import time


class GameRenderer:
    def __init__(self, screen, game_mode, images, button_images, background = (0, 100, 0)):
        if game_mode == "Klondike":
            game = Klondike()
        else:
            raise ValueError("Invalid game mode")
        self.game_mode = game_mode
        self.game = game
        self.screen = screen
        self.background = background
        self.card_images = images # Dictionary of card images
        self.button_images = button_images
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
        self.undo_button = ButtonImg(button_images["undo"], Dims())
        
        # Text
        self.moves_text = Text(Dims(), "Moves: 0", (0, 0, 0), (255, 255, 255), pygame.font.Font(None, 36))
        self.timer_text = Text(Dims(), "Time: 0", (0, 0, 0), (255, 255, 255), pygame.font.Font(None, 36))
        
        
        self.set_dimensions()
        
        self.states = deque()
        self.game.selected_card_overlay = pygame.Surface((self.dims["card"]["width"], self.dims["card"]["height"]))
        self.game.selected_card_overlay.set_alpha(128)  # Transparency level
        self.game.selected_card_overlay.fill((0, 0, 0))  # Black color
        self.game.selected_card_location = None
        self.game.moves = 0
        self.game.prevMoves = 0
        self.start_time = time.time()
        
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
        self.game.selected_card_overlay = pygame.Surface((self.dims["card"]["width"], self.dims["card"]["height"]))
        self.game.selected_card_overlay.set_alpha(128)  # Transparency level
        self.game.selected_card_overlay.fill((0, 0, 0))  # Black color
        self.dims["undo_button"]["width"] = self.dims["screen"]["width"] * 0.05
        self.dims["undo_button"]["height"] = self.dims["undo_button"]["width"]
        self.dims["undo_button"]["x"] = self.dims["undo_button"]["width"] * 0.5
        self.dims["undo_button"]["y"] = self.dims["undo_button"]["height"] * 0.5
        
        # Text Updates
        self.moves_text.update_dims(Dims(self.dims["screen"]["width"] * 0.3, self.dims["screen"]["height"] * 0.05, 0, 0))
        self.timer_text.update_dims(Dims(self.dims["screen"]["width"] * 0.6, self.dims["screen"]["height"] * 0.05, 0, 0))
        
        # Button Updates
        self.undo_button.update_dims(self.dims["undo_button"])
        
        '''End of set_dimensions()'''
        

    def update(self, mouse, click = "None"):
        
        # Store State Check
        if self.game.moves > self.game.prevMoves:
            self.store_state()
            self.game.prevMoves = self.game.moves
            
        # Update Moves Text
        self.moves_text.update_text(f"Moves: {self.game.moves}")
        
        # Update Timer Text
        self.timer_text.update_text(f"Time: {int(time.time() - self.start_time)}")
        
        if self.game.check_auto_complete():
            # Auto Complete
            # Add if statement to check if auto complete is approved by player
            # If approved, then auto complete
            # Add a button that is drawn only if self.can_auto_complete is True
            # Add self.perform_auto_complete var for the decision
            self.game.auto_complete()
        
        # Game Win Check
        if self.game.is_game_won():
            self.states.clear()
            self.game.moves = 0
            self.game.prevMoves = 0
            self.start_time = time.time()
            self.game.initialize_game()
            
        
        
        # Game Loss Check (To be implemented...)
            
        
        # Mouse Click Check
        clicked = self.check_click(mouse, click)
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
            if visible == 1 and len(self.game.stock.waste) == 1:
                self.game.stock.waste[-1].face_up()
                self.game.stock.waste[-1].pos.x = self.dims["waste"]["x"] + self.dims["waste"]["padding"]#######################################################    POSSIBLE FIX FOR VISIBILITY ERROR IN WASTE PILE     #############################################################################################################################################################################
                self.game.stock.waste[-1].pos.y = self.dims["waste"]["y"]
            else:
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
        
        # Text
        self.moves_text.draw(self.screen)
        self.timer_text.draw(self.screen)
        
        
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
                        self.screen.blit(self.game.selected_card_overlay, (card.pos.x, card.pos.y))
                    
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
                    self.screen.blit(self.game.selected_card_overlay, (foundation.pile[-1].pos.x, foundation.pile[-1].pos.y))
        
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
                    self.screen.blit(self.game.selected_card_overlay, (self.game.stock.waste[-1].pos.x, self.game.stock.waste[-1].pos.y))
        else:
            pygame.draw.rect(self.screen, (int(self.background[0] * 0.5), int(self.background[1] * 0.5), int(self.background[2] * 0.5)), (self.dims["waste"]["x"] + self.dims["card"]["width"] * 0.5, self.dims["waste"]["y"], self.dims["card"]["width"], self.dims["card"]["height"]))

        # Update Screen
        pygame.display.flip()
        '''End of draw()'''
    
   
    def check_click(self, mouse, click):
        # Checks if a click is valid
        # Returns the location of the click
            
        if self.undo_button.check_click(mouse.x, mouse.y):
            if click == "Up":
                self.undo_button.clear()
                return "Undo"
            elif click == "Down":
                self.undo_button.press()
            else:
                self.undo_button.hover()
        else:
            self.undo_button.clear()
        if click == "Up":
            # Tableau Clicked
            for colIdx, column in enumerate(self.game.tableau.tableau):
                if len(column) == 0:
                    rect_x = colIdx * self.dims["tableau"]["col_width"] + (self.dims["screen"]["width"] - self.dims["tableau"]["width"]) / 2
                    rect_y = self.dims["card"]["height"] * 1.33
                    if rect_x <= mouse.x <= rect_x + self.dims["card"]["width"] and rect_y <= mouse.y <= rect_y + self.dims["card"]["height"]:
                        return f"T{colIdx}E"
                for cdIdx, card in reversed(list(enumerate(column))):
                    if card.pos.x <= mouse.x <= card.pos.x + self.dims["card"]["width"] and card.pos.y <= mouse.y <= card.pos.y + self.dims["card"]["height"]:
                        return f"T{colIdx}{cdIdx}"
                    
            # Foundation clicked
            for i, foundation in enumerate(self.game.foundation):
                if foundation.pos.x <= mouse.x <= foundation.pos.x + self.dims["card"]["width"] and foundation.pos.y <= mouse.y <= foundation.pos.y + self.dims["card"]["height"]:
                    return f"F{i}"
            
            # Stock Clicked
            if self.dims["stock"]["x"] <= mouse.x <= self.dims["stock"]["x"] + self.dims["card"]["width"] and self.dims["stock"]["y"] <= mouse.y <= self.dims["stock"]["y"] + self.dims["card"]["height"]:
                return "S"
            
            # Waste Clicked
            if self.dims["waste"]["x"] + self.dims["card"]["width"] * 0.5 <= mouse.x <= self.dims["waste"]["x"] + self.dims["card"]["width"] * 2.5 and self.dims["waste"]["y"] <= mouse.y <= self.dims["waste"]["y"] + self.dims["card"]["height"]:
                return "W"
        return None
        '''End of check_click()'''
  
            
    def click_handler(self, clicked):
        # Handles a click
        # Clicked is the location of the current click
        # References self.game.selected_card_location as the previous click
        
        # Undo Clicked
        if clicked == "Undo":
            self.undo_state()
        
        # Double Clicked
        if self.game.selected_card_location == clicked:
            self.game.auto_move()
            return None
        
        # Tableau Clicked
        if clicked[0] == "T":
            colIdx = int(clicked[1])
            # Empty Pile Check
            if clicked[2:] == "E":
                cardIdx = clicked[2:]
            else:
                cardIdx = int(clicked[2:])
            if self.game.selected_card_location == clicked:
                self.game.unselect_card()
            elif self.game.selected_card_location == None:
                if cardIdx != "E":
                    if self.game.tableau.legal_selection(colIdx, cardIdx):
                        self.game.tableau.tableau[colIdx][cardIdx].select()
                        if len(self.game.tableau.tableau[colIdx]) > cardIdx + 1:
                            for i in range(cardIdx + 1, len(self.game.tableau.tableau[colIdx])):
                                self.game.tableau.tableau[colIdx][i].select()
                        else:
                            # Ace Check
                            if self.game.tableau.tableau[colIdx][cardIdx].rank == 'A':
                                self.game.move_card(clicked, f"FA")
                                self.game.selected_card_location = None
                                return None
                        self.game.selected_card_location = clicked
            elif self.game.selected_card_location[0] in ["F", "W", "T"]:
                self.game.move_card(self.game.selected_card_location, clicked)
            else:
                raise Exception("Selected card location is invalid")
            
        # Foundation Clicked
        elif clicked[0] == "F":
            if self.game.selected_card_location == clicked:
                self.game.unselect_card()
            elif self.game.selected_card_location == None:
                foundation = int(clicked[1])
                if len(self.game.foundation[foundation].pile) > 0:
                    self.game.foundation[foundation].pile[-1].select()
                    self.game.selected_card_location = clicked
            elif self.game.selected_card_location[0] in ["T", "F", "W"]:
                self.game.move_card(self.game.selected_card_location, clicked)
            else:
                raise Exception("Selected card location is invalid")
            
        # Stock Clicked
        elif clicked[0] == "S":
            self.game.stock.unselect_all("stock")
            self.game.stock.draw_card()
            self.game.unselect_card()
            self.game.moves += 1
        
        # Waste Clicked
        elif clicked[0] == "W":
            if self.game.selected_card_location != None or self.game.stock.waste_visible == 0:
                self.game.unselect_card()
            elif len(self.game.stock.waste) > 0:
                self.game.selected_card_location = clicked
                # Ace Check
                if self.game.stock.waste[-1].rank == 'A':
                    self.game.move_card(clicked, f"FA")
                    self.game.selected_card_location = None
                    return None
                self.game.stock.waste[-1].select()
        '''End of click_handler()'''

  
    def store_state(self):
        # Should I store any GameRenderer data?
        game_backup = self.game.backup()
        
        self.states.append(game_backup)
        '''End of store_state()'''
        
    def undo_state(self):
        if len(self.states) > 1:
            self.states.pop()
            self.game.restore(self.states[-1])
            self.game.moves += 2
            self.game.prevMoves = self.game.moves
            self.update(Pos())
            print("Undoing move. Undos left", len(self.states) - 1)
        else:
            print("Cannot undo any further")
        '''End of undo_state()'''
    
    '''
    def save_state(self):
        # For now saving state without history
        pass
        
        
        game_state = self.game.backup()
        with open(f"{self.game_mode}_SaveState.json", "w") as f:
            f.write(game_state)
        
    def load_state(self):
        Not implemented yet    
    '''


    
    
    
if __name__ == "__main__":
    raise Exception("This file is not meant to be ran directly!")


