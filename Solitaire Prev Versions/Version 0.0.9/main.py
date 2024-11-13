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
# 7. High score
# 8. Save game
# 9. Load game

# KLONDIKE SOLITAIRE RULES
# 1. 52 card deck
# 2. 7 tableau columns
# 3. 4 foundation piles
# 4. 1 waste pile
# 5. 1 stock pileh
# 6. 1 card is drawn from stock to waste
# 7. Move cards to foundation piles
# 8. Move cards to tableau columns
# 9. Build tableau columns in descending order
# 10. Build tableau columns in alternating colors
# 11. Build foundation piles in ascending order
# 12. Ace is low, King is high
# 13. Win by moving all cards to foundation piles
# 14. Winable state check (for during play as well as generation) (want to have an always winable feature)
# 15. Undo moves
# 16. Restart game


import numpy as np
import random
import os
import time
import sys
import pygame
from utils.classes import Card, Standard_Deck, Tableau, Foundation, Stock, Klondike, GameRenderer
from utils.definitions import *





# NOTE: Functions are all tested but not 100% confirmed to work
# Classes to Add
# Card - Done
# Deck - Done
# Tableau - Done
# Foundation - Done 
# Stock - Done
# Klondike - Done

'''
ISSUES / ADDITIONS
Issues:


Additions:
# Breakup classes.py into separate files 
# Display number of moves
# If ace clicked, auto move to foundation
# Double click feature (move to next available spot - priority based (f, t l-r))
# Hint Feature (unsure how to implement yet)
# Need an always winable variable and feature
# Optional auto complete feature (show button if available) when tableau only contains 4 full stacks ( might be able to check if tableau[0] is king and stock / waste is empty)
# Clean up prints
'''

# Initialize Pygame
pygame.init()

# Set up the display
#screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
screen = pygame.display.set_mode((1920, 1080), pygame.RESIZABLE)

pygame.display.set_caption("Klondike Solitaire")

# Constants
FPS = 60


# Simple Classes
class Mouse:
    def __init__(self):
      self.x = -1
      self.y = -1



# Game Loop



def game():
    # Initialize game
    klondike = Klondike()
    curr_card_path = CARD_PATHS_CLASSIC
    curr_btn_path = BUTTON_PATHS
    def_bg_color = (0, 100, 0)
    renderer = GameRenderer(klondike, screen, curr_card_path, curr_btn_path, def_bg_color)
    clock = pygame.time.Clock()
    mouse = Mouse()
    # Main game loop
    running = True
    while running:
        clock.tick(FPS)
        
        
        mouse.x = mouse.y = None 
        
        for event in pygame.event.get():
          
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    mouse.x, mouse.y = pygame.mouse.get_pos()
              
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