# Want UI
# Start with classic solitaire
# Use sprite sheets for card images
# Use Pygame for UI
# import pygame
# FEATURES
# 1. Draw 1 or 3 cards
# 2. Move cards
# 3. Win condition (always_winable feature)
# 4. Restart game
# 5. Undo moves
# 6. Timer
# 8. Save game
# 9. Load game



import numpy as np # type: ignore
import random
import os
import time
import sys
import pygame # type: ignore
from GameRenderer import GameRenderer
from utils.classes.misc import Mouse
from utils.definitions import *



'''
ISSUES / ADDITIONS
Issues:
# Waste card stuck face down near end of game - In this case it was a 3 of clubs - Seems to be an issue with the visibility of the waste pile - Attempted a fix, doesnt seem to work - happens very rarely
# Undo is bugged again - If I undo and then repeat action, then undo again, it wont work
# Consider moving the move_card and auto_move function to the klondike class

Additions:
# Display time elapsed - Partial; Font Issues, want m:s time
# Display number of moves - Partial; Font Issues
# Clean up prints - Done
# If ace clicked, auto move to foundation - Done - Testing Still
# Double click feature (move to next available spot - priority based (f, t l-r)) - Done - Testing Still

# Optional auto complete feature (show button if available) when tableau only contains 4 full stacks ( might be able to check if tableau[0] is king and stock / waste is empty) - 
           Maybe make it a toggle that allows for auto movement to foundation at all times (would naturally auto complete at end of game but player can choose to enable it earlier)
# Save and Load Game feature
# Drag feature
# Spider Solitaire
# Hint Feature (unsure how to implement yet)
    2 Ideas:
        1. Find all possible moves and using a priority system, suggest move to best spot
        2. Suggest first possible move found or stock pile click if no moves found
    Could alternatively just make a help button that performs a move for the player, without suggesting it first
# Need an always winable variable and feature 
    Can either generate a random deck, and have an ai play it to completion, and add it to a json or similar file that can store the start state of the winnable games
    Or can have an algorithm that reverses the game from the end state to the start state and uses that (would not have to store it in a JSON)
    May not need to use a storage feature either way

# Main Menu
# Add a settings menu

# Buttons to go from main menu to settings to game, and vice versa

# Spider Solitaire
# Free Cell
# Tri Peaks Solitaire


'''

# Initialize Pygame
pygame.init()

# Set up the display
#screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
screen = pygame.display.set_mode((1920, 1080), pygame.RESIZABLE)

pygame.display.set_caption("Klondike Solitaire")

# Constants
FPS = 60
DOUBLE_CLICK_TIME = 0.3






# Game Loop



def game():
    # Initialize game
    game_mode = "Klondike"
    curr_card_path = CARD_PATHS_CLASSIC
    curr_btn_path = BUTTON_PATHS
    def_bg_color = (0, 100, 0)
    renderer = GameRenderer(game_mode, screen, curr_card_path, curr_btn_path, def_bg_color)
    clock = pygame.time.Clock()
    mouse = Mouse(DOUBLE_CLICK_TIME)
    # Main game loop
    running = True
    while running:
        clock.tick(FPS)
        
        
        mouse.x = mouse.y = None 
        
        for event in pygame.event.get():
          
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    mouse.x, mouse.y = pygame.mouse.get_pos()
                    mouse.check_double_click()
                        
              
            if event.type == pygame.VIDEORESIZE:
                renderer.set_dimensions()
                renderer.screen = screen
            
            if event.type == pygame.QUIT:
              running = False
              
        # Update Renderer
        renderer.update(mouse)
    pygame.quit()
  
if __name__ == "__main__":
  game()