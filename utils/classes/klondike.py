'''
~~~~ klondike.py ~~~~

Contains the Klondike class for the game (acts as a wrapper to use the other 
                                            classes in tandem and operate 
                                                based on the rules of klondike)

Functions:
    __init__(): Initializes the Klondike object with the given background, card images, button images, and screen.
    __repr__(): Returns a string representation of the Klondike object.
    is_game_won(): Checks if the game has been won.
    check_auto_complete(): Checks if the game can be auto completed.
    set_dimensions(): Sets the dimensions of the game elements.
    initialize_game(): Initializes the game by shuffling the deck and dealing the initial cards.
    unselect_card(): Unselects the selected card.
    update(): Updates the game based on the mouse position and click state.
    pos_cards(): Sets the position of each card based on its location.
    draw(): Draws all cards to the screen based on their positions.
    check_click(): Checks if a click is valid.
    click_handler(): Handles a click based on the location of the click.
    vector_distance(): Returns the distance between two Pos objects.
    move_card(): Moves a card from one location to another.
    auto_complete(): Automatically completes the game.
    store_state(): Stores the current state of the game.
    undo_state(): Undoes the last move made in the game.
    backup(): Backs up the current state of the game.
    restore(): Restores the game to a previous state.
    
    
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
from pygame.locals import *
import pygame
from .ui import ButtonImg, Text
from .misc import Dims, Mouse, Pos
import time
from collections import deque


class Klondike:
    # Will want to add a win check
    # Will want to add a legal move check
    # Will want to add a winable check for init
    def __init__(self, background, card_images, button_images, screen):
        self.deck = Standard_Deck()
        self.tableau = Tableau()
        self.foundation = [Foundation() for _ in range(4)]
        self.stock = Stock()
        self.moves = 0
        self.prevMoves = 0
        self.selected_card_location = None
        self.selected_card_overlay = None
        self.dragging = False
        self.last_click = "None"
        
        
        self.selected_card_location = None
        self.moves = 0
        self.prevMoves = 0
        self.start_time = time.time()
        
        self.dims = {
            "screen": {"width": 0, "height": 0},
            "card": {"width": 0, "height": 0},
            "tableau": {"width_proportion": 0, "height_proportion": 0, "padding": 0, "width": 0, "height": 0, "col_width": 0},
            "foundation": {"padding": 0},
            "stock": {"x": 0, "y": 0},
            "waste": {"x": 0, "y": 0},
            "undo_button": {"x": 0, "y": 0, "width": 0, "height": 0}
        }
        
        # UI
        self.screen = screen
        self.selected_card_overlay = pygame.Surface((self.dims["card"]["width"], self.dims["card"]["height"]))
        self.selected_card_overlay.set_alpha(128)  # Transparency level
        self.selected_card_overlay.fill((0, 0, 0))  # Black color
        self.background = background
        self.card_images = card_images # Dictionary of card images
        self.button_images = button_images
        
        # Buttons
        self.undo_button = ButtonImg(button_images["undo"], Dims())
        
        # Text
        self.moves_text = Text(Dims(), "Moves: 0", (0, 0, 0), (255, 255, 255), pygame.font.Font(None, 36))
        self.timer_text = Text(Dims(), "Time: 0", (0, 0, 0), (255, 255, 255), pygame.font.Font(None, 36))
        
        
        self.set_dimensions()
        self.initialize_game()
        self.states = deque()
        self.store_state()
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

    def set_dimensions(self):
        # Sets all the dimensions to the default settings
        # Based on screen size to be scalable
        
        # Dims Updates
        self.dims["screen"]["width"], self.dims["screen"]["height"] = self.screen.get_size()
        self.dims["card"]["height"] = self.dims["screen"]["height"] * 0.15
        self.dims["card"]["width"] = self.dims["card"]["height"] * 0.7
        self.dims["tableau"]["width_ratio"] = 0.55
        self.dims["tableau"]["height_ratio"] = 0.24
        self.dims["tableau"]["width"] = self.dims["screen"]["width"] * self.dims["tableau"]["width_ratio"]
        self.dims["tableau"]["height"] = self.dims["screen"]["height"] * self.dims["tableau"]["height_ratio"]
        self.dims["tableau"]["col_width"] = self.dims["tableau"]["width"] / self.tableau.columns()
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
        
        # Text Updates
        self.moves_text.update_dims(Dims(self.dims["screen"]["width"] * 0.3, self.dims["screen"]["height"] * 0.05, 0, 0))
        self.timer_text.update_dims(Dims(self.dims["screen"]["width"] * 0.6, self.dims["screen"]["height"] * 0.05, 0, 0))
        
        # Button Updates
        self.undo_button.update_dims(self.dims["undo_button"])
        
        '''End of set_dimensions()'''

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
    
    
    def update(self, mouse, click):
    
        # Store State Check
        if self.moves > self.prevMoves:
            self.store_state()
            self.prevMoves = self.moves
        
        # Update Moves Text
        self.moves_text.update_text(f"Moves: {self.moves}")
        
        # Update Timer Text
        self.timer_text.update_text(f"Time: {int(time.time() - self.start_time)}")
        
        if self.check_auto_complete():
            # Auto Complete
            # Add if statement to check if auto complete is approved by player
            # If approved, then auto complete
            # Add a button that is drawn only if self.can_auto_complete is True
            # Add self.perform_auto_complete var for the decision
            self.auto_complete()
        
        # Mouse Click Check
        
        clicked = self.check_click(mouse, click)
        if clicked != None:
            self.click_handler(clicked, click)
            
            # Check if a card was clicked
            # Select that card (either internally, externally, or both)
        else:
            if click == "Up" or click == "Down":
                self.dragging = False
                self.unselect_card()
    
        if not mouse.leftClickState and self.dragging:
            self.dragging = False
        
        # Card Positioning
        self.pos_cards()
        
        # Draw To Screen
        self.draw(mouse)
        '''End of update()'''
    
    
    def pos_cards(self):
        # Sets the pos of each card depending on its location
        
        # Tableau Cards
        for col_index, column in enumerate(self.tableau.tableau):
            if len(column) != 0:
                chg = (self.dims["tableau"]["height"] / (self.tableau.largest_column() / 2))
                for row_index, card in enumerate(column):
                    card.pos.x = col_index * self.dims["tableau"]["col_width"] + (self.dims["screen"]["width"] - self.dims["tableau"]["width"]) / 2
                    card.pos.y = row_index * min(chg, self.dims["card"]["height"] * 0.5) + self.dims["card"]["height"] * 1.33
        
        # Foundation Cards
        x_start = (self.dims["screen"]["width"] - (self.dims["card"]["width"] + self.dims["foundation"]["padding"]) * 4) - self.dims["card"]["width"]
        y_start = self.dims["card"]["height"] * self.dims["foundation"]["padding"]
        for i, foundation in enumerate(self.foundation):
            foundation.pos.x = x_start + i * (self.dims["card"]["width"] + self.dims["foundation"]["padding"] * self.dims["card"]["width"])
            foundation.pos.y = y_start
            if len(foundation.pile) > 0:
                for card in foundation.pile:
                    card.pos.x = foundation.pos.x
                    card.pos.y = foundation.pos.y
        
        
        
        # Stock Cards
        self.stock.set_face_down("all")
        for card in self.stock.stock:
            card.pos.x = self.dims["stock"]["x"]
            card.pos.y = self.dims["stock"]["y"]
        
        # Waste Cards
        if len(self.stock.waste) > 0:
            visible = min(3, len(self.stock.waste)) # Number of visible cards in waste pile
            self.stock.set_face_down("waste") # Face down all cards in waste pile

            for i in range(visible):
                self.stock.waste[-(i + 1)].face_up()
                self.stock.waste[-(i + 1)].pos.x = self.dims["waste"]["x"] + (visible - i) * self.dims["waste"]["padding"]
                self.stock.waste[-(i + 1)].pos.y = self.dims["waste"]["y"]
        '''End of pos_cards()'''
    
    
    def draw(self, mouse):
        # Draws all cards to the screen based on their positions
        drag_vector_limit = self.dims["card"]["height"] * 0.3
        
        # Background
        self.screen.fill(self.background)
        
        # Buttons
        self.undo_button.draw(self.screen)
        
        # Text
        self.moves_text.draw(self.screen)
        self.timer_text.draw(self.screen)
        
        drag_draw = []
        
        # Tableau
        for colIdx, column in enumerate(self.tableau.tableau):
            
            # generate a rect the size of the column, that is a darker color than self.background
            # draw the rect
            rect_x = colIdx * self.dims["tableau"]["col_width"] + (self.dims["screen"]["width"] - self.dims["tableau"]["width"]) / 2
            rect_y = self.dims["card"]["height"] * 1.33
            pygame.draw.rect(self.screen, (int(self.background[0] * 0.5), int(self.background[1] * 0.5), int(self.background[2] * 0.5)), (rect_x, rect_y, self.dims["card"]["width"], self.dims["card"]["height"]))
            
            if len(column) > 0:
                for idx, card in enumerate(column):
                    if not card.is_selected() or not self.dragging:
                        # Normal Draw
                        if card.is_face_up():
                            card_image = self.card_images[card.id]
                        else:
                            card_image = self.card_images['back']
                        card_image = pygame.transform.scale(card_image, (int(self.dims["card"]["width"]), int(self.dims["card"]["height"])))
                        self.screen.blit(card_image, (card.pos.x, card.pos.y))
                        if card.is_selected():
                            self.screen.blit(self.selected_card_overlay, (card.pos.x, card.pos.y))
                    else:
                        break
                    
                prevIdx = idx
                use_mouse_pos = self.vector_distance(column[prevIdx].pos, mouse) > drag_vector_limit and self.dragging and column[prevIdx].is_selected()
                if use_mouse_pos:
                    drag_x = mouse.x - self.dims["card"]["width"] * 0.5
                    drag_y = mouse.y - self.dims["card"]["height"] * 0.2
                else:
                    drag_x = column[prevIdx].pos.x
                    drag_y = column[prevIdx].pos.y
                    
                for idx, card in enumerate(column[prevIdx:]):
                    if use_mouse_pos:
                        card_image = self.card_images[card.id]
                        drag_draw.append((card_image, drag_x, drag_y))
                        drag_y += self.dims["card"]["height"] * 0.2
                    else:
                            # Normal Unselected Draw
                        if card.is_face_up():
                            card_image = self.card_images[card.id]
                        else:
                            card_image = self.card_images['back']
                        card_image = pygame.transform.scale(card_image, (int(self.dims["card"]["width"]), int(self.dims["card"]["height"])))
                        self.screen.blit(card_image, (card.pos.x, card.pos.y))
                        if card.is_selected():
                            self.screen.blit(self.selected_card_overlay, (card.pos.x, card.pos.y))
                            
                    
        # Foundation
        for foundation in self.foundation:
            
            pygame.draw.rect(self.screen, (int(self.background[0] * 0.5), int(self.background[1] * 0.5), int(self.background[2] * 0.5)), (foundation.pos.x, foundation.pos.y, self.dims["card"]["width"], self.dims["card"]["height"]))

            if len(foundation.pile) > 0:
                idx = len(foundation.pile) - 1
                if foundation.pile[idx].is_selected() and self.dragging and self.vector_distance(foundation.pile[idx].pos, mouse) > drag_vector_limit:
                    if len(foundation.pile) > 1:
                        idx -= 1
                    else:
                        pygame.draw.rect(self.screen, (int(self.background[0] * 0.5), int(self.background[1] * 0.5), int(self.background[2] * 0.5)), (foundation.pos.x, foundation.pos.y, self.dims["card"]["width"], self.dims["card"]["height"]))

                # Normal Draw (Draws the top card or the card below it if needed)
                if not foundation.pile[idx].is_selected() or not self.dragging or self.vector_distance(foundation.pile[idx].pos, mouse) <= drag_vector_limit:
                    if not foundation.pile[idx].is_face_up():
                        foundation.pile[idx].face_up()
                    card_image = self.card_images[foundation.pile[idx].id]
                    card_image = pygame.transform.scale(card_image, (int(self.dims["card"]["width"]), int(self.dims["card"]["height"])))
                    self.screen.blit(card_image, (foundation.pos.x, foundation.pos.y))
                    if foundation.pile[idx].is_selected():
                        self.screen.blit(self.selected_card_overlay, (foundation.pile[idx].pos.x, foundation.pile[idx].pos.y))

                if foundation.pile[-1].is_selected() and self.dragging and self.vector_distance(foundation.pile[-1].pos, mouse) > drag_vector_limit:
                    # Draw the top card as a drag
                    drag_x = mouse.x - self.dims["card"]["width"] * 0.5
                    drag_y = mouse.y - self.dims["card"]["height"] * 0.2
                    card_image = self.card_images[foundation.pile[-1].id]
                    drag_draw.append((card_image, drag_x, drag_y))
        
        # Stock
        pygame.draw.rect(self.screen, (int(self.background[0] * 0.5), int(self.background[1] * 0.5), int(self.background[2] * 0.5)), (self.dims["stock"]["x"], self.dims["stock"]["y"], self.dims["card"]["width"], self.dims["card"]["height"]))
        if len(self.stock.stock) > 0:
            card_image = self.card_images['back']
            card_image = pygame.transform.scale(card_image, (int(self.dims["card"]["width"]), int(self.dims["card"]["height"])))
            self.screen.blit(card_image, (self.dims["stock"]["x"], self.dims["stock"]["y"]))
        

        
        # Waste
        pygame.draw.rect(self.screen, (int(self.background[0] * 0.5), int(self.background[1] * 0.5), int(self.background[2] * 0.5)), (self.dims["waste"]["x"] + self.dims["card"]["width"] * 0.5, self.dims["waste"]["y"], self.dims["card"]["width"], self.dims["card"]["height"]))
        
        if len(self.stock.waste) > 0:
            visible = min(3, len(self.stock.waste))
            
            for i in reversed(range(visible)):
                self.stock.waste[-(i + 1)].face_up()
                if i == 0 and self.stock.waste[-1].is_selected() and self.dragging and self.vector_distance(self.stock.waste[-1].pos, mouse) > drag_vector_limit:
                    # Drag Draw
                    drag_x = mouse.x - self.dims["card"]["width"] * 0.5
                    drag_y = mouse.y - self.dims["card"]["height"] * 0.2
                    card_image = self.card_images[self.stock.waste[-1].id]
                    drag_draw.append((card_image, drag_x, drag_y))
                
                else:
                    # Normal Draw
                    
                    card_image = self.card_images[self.stock.waste[-(i + 1)].id]
                    card_image = pygame.transform.scale(card_image, (int(self.dims["card"]["width"]), int(self.dims["card"]["height"])))
                    self.screen.blit(card_image, (self.stock.waste[-(i + 1)].pos.x, self.stock.waste[-(i + 1)].pos.y))
                    if self.stock.waste[-(i + 1)].is_selected():
                        # Draw a transparent rectangle over card
                        # Rectangle should be dark
                        self.screen.blit(self.selected_card_overlay, (self.stock.waste[-(i + 1)].pos.x, self.stock.waste[-(i + 1)].pos.y))
        
        
        # Drag Draw
        for card_image, x, y in drag_draw:
            card_image = pygame.transform.scale(card_image, (int(self.dims["card"]["width"]), int(self.dims["card"]["height"])))
            self.screen.blit(card_image, (x, y))
            self.screen.blit(self.selected_card_overlay, (x, y))

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
        if click == "Up" or click == "Down":
            # Tableau Clicked
            for colIdx, column in enumerate(self.tableau.tableau):
                if len(column) == 0:
                    rect_x = colIdx * self.dims["tableau"]["col_width"] + (self.dims["screen"]["width"] - self.dims["tableau"]["width"]) / 2
                    rect_y = self.dims["card"]["height"] * 1.33
                    if rect_x <= mouse.x <= rect_x + self.dims["card"]["width"] and rect_y <= mouse.y <= rect_y + self.dims["card"]["height"]:
                        print(f"Tableau {colIdx} Clicked: Empty")
                        return f"T{colIdx}E"
                for cdIdx, card in reversed(list(enumerate(column))):
                    if card.pos.x <= mouse.x <= card.pos.x + self.dims["card"]["width"] and card.pos.y <= mouse.y <= card.pos.y + self.dims["card"]["height"]:
                        print(f"Tableau {colIdx} Clicked: {self.tableau.tableau[colIdx][cdIdx]}")
                        return f"T{colIdx}{cdIdx}"
                    
            # Foundation clicked
            for i, foundation in enumerate(self.foundation):
                if foundation.pos.x <= mouse.x <= foundation.pos.x + self.dims["card"]["width"] and foundation.pos.y <= mouse.y <= foundation.pos.y + self.dims["card"]["height"]:
                    print(f"Foundation {i} Clicked")
                    return f"F{i}"
            
            # Stock Clicked
            if self.dims["stock"]["x"] <= mouse.x <= self.dims["stock"]["x"] + self.dims["card"]["width"] and self.dims["stock"]["y"] <= mouse.y <= self.dims["stock"]["y"] + self.dims["card"]["height"]:
                print("Stock Clicked")
                return "S"
            
            # Waste Clicked
            if self.dims["waste"]["x"] + self.dims["card"]["width"] * 0.5 <= mouse.x <= self.dims["waste"]["x"] + self.dims["card"]["width"] * 2.5 and self.dims["waste"]["y"] <= mouse.y <= self.dims["waste"]["y"] + self.dims["card"]["height"]:
                print("Waste Clicked")
                return "W"
        return None
        '''End of check_click()'''
  
            
    def click_handler(self, clicked, click_state): 
        # Handles a click
        # Clicked is the location of the current click
        # References self.selected_card_location as the previous click
        
        # Undo Clicked
        if clicked == "Undo":
            self.undo_state()
            return None
        
        # Same Card Clicked
        if self.selected_card_location == clicked:
            if click_state == "Up":
                self.dragging = False
                return None
            if click_state == "Down":
                if self.dragging:
                    raise Exception("Clicked on same card but dragging is still True")
                print("Performing Auto Move")
                self.auto_move()
            return None
        
        # Tableau Clicked
        if clicked[0] == "T":
            colIdx = int(clicked[1])
            # Empty Pile Check
            if clicked[2:] == "E":
                cardIdx = clicked[2:]
            else:
                cardIdx = int(clicked[2:])
            if self.selected_card_location == None:
                # No previous card selected - Attempt to select this one
                if cardIdx != "E" and click_state == "Down":
                    if self.tableau.legal_selection(colIdx, cardIdx):
                        self.tableau.tableau[colIdx][cardIdx].select()
                        if len(self.tableau.tableau[colIdx]) > cardIdx + 1:
                            for i in range(cardIdx + 1, len(self.tableau.tableau[colIdx])):
                                self.tableau.tableau[colIdx][i].select()
                        else:
                            # Ace Check
                            if self.tableau.tableau[colIdx][cardIdx].rank == 'A':
                                self.move_card(clicked, f"FA")
                                # self.selected_card_location = None
                                self.unselect_card()
                                self.dragging = False
                                return None
                        self.selected_card_location = clicked
                        self.dragging = True
            elif self.selected_card_location[0] in ["F", "W", "T"]:
                if click_state == "Up":
                    # Click State is Up
                    if self.dragging:
                        self.move_card(self.selected_card_location, clicked)
                        self.dragging = False
                else:
                    # Click State is Down
                    if self.dragging:
                        raise Exception("Dragging is True but click state is Down")
                    self.move_card(self.selected_card_location, clicked)
            else:
                raise Exception("Selected card location is invalid")
            
        # Foundation Clicked
        elif clicked[0] == "F":
            if self.selected_card_location == None:
                foundIdx = int(clicked[1])
                if len(self.foundation[foundIdx].pile) > 0 and click_state == "Down":
                    self.foundation[foundIdx].pile[-1].select()
                    self.selected_card_location = clicked
                    self.dragging = True
            elif self.selected_card_location[0] in ["T", "F", "W"]:
                if click_state == "Up":
                    if self.dragging:
                        self.move_card(self.selected_card_location, clicked)
                        self.dragging = False
                else:
                    if self.dragging:
                        raise Exception("Dragging is True but click state is Down")
                    self.move_card(self.selected_card_location, clicked)
            else:
                raise Exception("Selected card location is invalid")
            
        # Stock Clicked
        elif clicked[0] == "S" and click_state == "Down":
            self.stock.unselect_all("all")
            self.stock.draw_card()
            self.unselect_card()
            self.moves += 1
            self.dragging = False
        
        # Waste Clicked
        elif clicked[0] == "W":
            if self.selected_card_location != None:
                print("Card Location is not None when Waste Pile Clicked")
                print(f"Selected Card Location: {self.selected_card_location}")
                print("")
                print("")
                self.unselect_card()
                self.dragging = False
            elif len(self.stock.waste) > 0:
                if click_state == "Down":
                    print("Down Action")
                    self.selected_card_location = clicked
                    print(f"Selected Card Location: {self.selected_card_location}")
                    # Ace Check
                    if self.stock.waste[-1].rank == 'A':
                        self.move_card(clicked, f"FA")
                        self.unselect_card()
                        return None
                    self.stock.waste[-1].select()
                    print("Selected Card")
                    print("")
                    print("")
                    self.dragging = True
        '''End of click_handler()'''


    def vector_distance(self, mouse, pos):
        # Returns the distance between two Pos objects
        pos2 = Pos(mouse.x + self.dims["card"]["width"] * 0.5, mouse.y + self.dims["card"]["height"] * 0.5)
        return ((pos.x - pos2.x) ** 2 + (pos.y - pos2.y) ** 2) ** 0.5
        '''End of vector_distance()'''
 



        
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
            else:
                raise ValueError("Invalid end location")
            self.unselect_card()
            
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
        self.unselect_card() # Potentially redundant
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
    
    
    def store_state(self):
        game_backup = self.backup()
        
        self.states.append(game_backup)
        '''End of store_state()'''
        
        
    def undo_state(self):
        if len(self.states) > 1:
            moves = self.moves
            self.states.pop()
            self.restore(self.states[-1])
            self.moves = moves + 1
            self.prevMoves = self.moves
            self.update(Mouse(), "None")
            print("Undoing move. Undos left", len(self.states) - 1)
        else:
            print("Cannot undo any further")
        '''End of undo_state()'''
    
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