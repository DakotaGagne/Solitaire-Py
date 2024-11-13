'''
~~~~ gameRenderer.py ~~~~

Contains the GameRenderer class for the game
Interacts with main.py to render the game
Will be used to handle all game types ("Klondike", "Spider", etc)
Will not be used to handle menu or non game rendering

Functions:
    __init__(): Initializes the GameRenderer object with the given screen, game mode, card images, button images, and default background color.
    update(): Updates the game based on the mouse position and click state.
    set_dimensions(): Updates the dimensions of the game elements.

Variables:
    screen: The screen object that the game will be rendered on.
    game_mode: A string that represents the game mode that the player is playing.
    card_images: A dictionary that contains the images for the cards in the game.
    button_images: A dictionary that contains the images for the buttons in the game.
    background: The default background color for the game.
    game: The game object that will be rendered on the screen.
    
'''

import pygame # type: ignore
from pygame.locals import * # type: ignore
from collections import deque
from copy import deepcopy
from ..classes.misc import Pos, Dims, Mouse
from ..classes.ui import ButtonImg, Text
from ..classes.klondike import Klondike
from ..classes.spider import Spider
from ..classes.freecell import Freecell
import time


class GameRenderer:
    def __init__(self, screen, game_mode, card_images, button_images, background = (0, 100, 0)):
        if game_mode == "Klondike":
            game = Klondike(background, card_images, button_images, screen)
        elif game_mode == "Spider":
            game = Spider(background, card_images, button_images, screen)
        elif game_mode == "Freecell":
            game = Freecell(background, card_images, button_images, screen)
        else:
            raise ValueError("Invalid game mode")
        self.game_mode = game_mode
        self.game = game
        self.card_images = card_images
        self.button_images = button_images
        self.background = background
           

    def update(self, mouse, click = "None"):
        # Game Win Check
        if self.game.is_game_won():
            self.game.states.clear()
            self.game.moves = 0
            self.game.prevMoves = 0
            self.game.start_time = time.time()
            self.game.initialize_game()
        
        # Game Loss Check (To be implemented...)
        
        self.game.update(mouse, click)
        
        '''End of update()'''
    
    def set_dimensions(self):
        self.game.set_dimensions()
      

    
    
if __name__ == "__main__":
    raise Exception("This file is not meant to be ran directly!")


