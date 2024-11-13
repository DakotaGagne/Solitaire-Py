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
from utils.Renderers.GameRenderer import GameRenderer
from utils.Renderers.MainMenuRenderer import MainMenuRenderer
from utils.Renderers.SettingsMenuRenderer import SettingsMenuRenderer
from utils.Renderers.PauseMenuRenderer import PauseMenuRenderer
from utils.classes.misc import Mouse
from utils.definitions import *
from utils.classes.ui import ButtonImg, ButtonRect

# Initialize Pygame
pygame.init()

# Set up the display
#screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
screen = pygame.display.set_mode((1000, 600), pygame.RESIZABLE)

pygame.display.set_caption("Solitaire - Created by Dakota G")

# Constants
FPS = 60
DOUBLE_CLICK_TIME = 0.3
GAME_MODES = ["Klondike", "Spider"]

# Game Loop



# Maybe make main_loop into a class and seperate the stuff in the loop into functions
def main_loop():
    # Initialize game
    curr_card_path = CARD_PATHS_CLASSIC
    curr_btn_path = BUTTON_PATHS
    def_bg_color = (0, 100, 0)
    clock = pygame.time.Clock()
    mouse = Mouse(DOUBLE_CLICK_TIME)
    gameMode = ""
    gameRenderer = None
    menuRenderer = MainMenuRenderer(screen, GAME_MODES, def_bg_color)
    settingsRenderer = SettingsMenuRenderer()
    pauseRenderer = PauseMenuRenderer()
    
    # window var refers to which window is the active one
    # 0 = Main Menu
    # 1 = Settings Menu
    # 2 = Pause Menu
    # 3 = Game Window
    window = "Main"
    # Maybe change window to be string ("main", "settings", "pause", "game")
    # Main game loop
    running = True
    
    click = "None"
    prev_mouse_state = False
    
    while running:
        clock.tick(FPS)
        mouse.x, mouse.y = pygame.mouse.get_pos()
        
        mouse_state = pygame.mouse.get_pressed()[0]
        
        # Event Loop
        for event in pygame.event.get():
              
            if event.type == pygame.VIDEORESIZE:
                if gameRenderer is not None:
                    gameRenderer.screen = screen
                    gameRenderer.set_dimensions()
                menuRenderer.screen = screen
                menuRenderer.updateDims()
                # add menu, settings and pause renderer resizing
            
            if event.type == pygame.QUIT:
              running = False
              break
        
        # Mouse Handling
        if mouse_state and not prev_mouse_state:
            click = "Down"
        elif not mouse_state and prev_mouse_state:
            click = "Up"
        else:
            click = "None"
        prev_mouse_state = mouse_state
             
        # Update Renderer
        
        
        if window == "Main":
            # Render Main Menu
            # Returns None if no change, otherwise Returns "Quit" if game is to be exited
            # Otherwise returns the window or the game mode
            res = menuRenderer.update(mouse, click)
            if res != None:
                if res == "Quit":
                    running = False
                elif res == "Settings":
                    print("Settings Switcher to Be Implemented")
                    pass
                else:
                    window = "Game"
                    gameMode = res
                    gameRenderer = GameRenderer(screen, gameMode, curr_card_path, curr_btn_path)
                    click = "None"
            
        elif window == "Settings":
            window = "Game"
            # Render Settings Menu
        elif window == "Pause":
            window = "Game"
            # Render Pause Menu
        elif window == "Game":
            if gameMode != "" and gameRenderer is not None:
                # Render Game Window
                res = gameRenderer.update(mouse, click)
                if res != None:
                    window = res
                    
            else:
                window = "Main"
    pygame.quit()
    
    


if __name__ == "__main__":
  main_loop()