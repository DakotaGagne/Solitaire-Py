'''
MainMenuRenderer.py

This file contains the MainMenuRenderer class which is used to render the main menu of the game. 
The main menu contains buttons for the different game modes, settings, and quitting the game. 
The buttons have hover effects, click effects, and will be able to scale to the window size. 
The main menu will also contain a title at the top center of the screen, and credits at the top left and top right of the screen.

Variables:
    screen: The screen object that the main menu will be rendered on.
    game_modes: A list of strings that represent the different game modes that the player can choose from.
    def_text_col: The default text color for the buttons.
    def_background_col: The default background color for the main menu.
    game_buttons: A list of ButtonImg objects that represent the buttons for the different game modes.
    font: The font object that will be used to render the text on the buttons.
    dims: A dictionary that contains the dimensions of the buttons and other elements on the main menu.
    buttonImg: The image file path for the buttons.
    settingImg: The image file path for the settings button.
    quitImg: The image file path for the quit button.

Functions:
    __init__(): Initializes the MainMenuRenderer object with the given screen, game modes, and default background color.
    updateDims(): Updates the dimensions of the buttons and other elements on the main menu.
    update(): Updates the main menu based on the mouse position and click state.
    draw(): Draws the main menu on the screen.
    check_mouse(): Checks for mouse events on the main menu.
    check_collision(): Checks for collision between the mouse and a button on the main menu.
    changeBGColor(): Changes the background color of the main menu.
    changeBtnColor(): Changes the button color of the main menu.
    changeTextColor(): Changes the text color of the buttons on the main menu.
    changeFont(): Changes the font of the text on the buttons on the main menu.

'''










from ..classes.ui import ButtonImg
from ..classes.misc import Dims
from ..definitions import *
from pygame.locals import *
import pygame





'''
Add Title
Use Images for the buttons
Get Images with hover and click effects
Overlay button with text if need be
Font should be resizeable

Add click, hover, and press functions to determine what is happening
Complete





'''


# Add text top center - SOLITATIRE
# Add Credits to top left (Me) and top right (Sav)



# Dims NEED to be fixed, looks like shit. For now focused on making it functional
# Update Buttons to what Sav makes when Sav makes it

class MainMenuRenderer:
    
    def __init__(self, screen, game_modes, def_bg_color = (0, 100, 0)):
        # Need buttons for the game choices, settings, and quit
        # Settings is gear Icon in Top left
        # Quit is X in top  right
        # Game choices are in the center
        # Buttons should have hover effects
        # Buttons should have a click effect
        # Maintain window size when entering the game
        # Buttons should scale to window size
        
        self.buttonImg = BUTTON_PATHS["blank"]
        self.settingImg = BUTTON_PATHS["settings"]
        self.quitImg = BUTTON_PATHS["quit"]
        
        
        self.screen = screen
        self.game_modes = game_modes
        self.def_text_col = (255, 255, 255)
        self.def_background_col = def_bg_color
        self.game_buttons = []
        self.font = pygame.font.Font(None, 36)
        
        # Initialize Dims
        self.dims = {"width": 0, "height": 0, "x": 0, "y": 0, "padding": 0, "font_size": 0}
        
        # Initialize Buttons
        for text in game_modes:
            self.game_buttons.append(ButtonImg(self.buttonImg, Dims(), {"text": text, "text_color": self.def_text_col, "font": self.font}))
        self.settings_button = ButtonImg(self.settingImg, Dims())
        self.quit_button = ButtonImg(self.quitImg, Dims())
        
        self.updateDims()
        
        
        
        # add hover feature to button classes
        # add click feature to button classes
    
    
    def updateDims(self):
        # Update font size in future as well
        self.dims["height"] = self.screen.get_height() / (2*(len(self.game_buttons) + 2))
        self.dims["width"] = self.dims["height"] * 3
        self.dims["padding"] = (self.screen.get_height() - (self.dims["height"] * (len(self.game_buttons)+2))) / (len(self.game_buttons)+5)
        self.dims["x"] = self.screen.get_width() / 2 - self.dims["width"] / 2
        self.dims["y"] = self.dims["padding"] * 3
        self.dims["font_size"] = int(self.dims["height"] / 2)
        
        dims = Dims(self.dims["x"], self.dims["y"], self.dims["width"], self.dims["height"])
        for idx, btn in enumerate(self.game_buttons):
            btn.update_dims(Dims(self.dims["x"], self.dims["y"] + (idx * (self.dims["height"] + self.dims["padding"])),\
                self.dims["width"], self.dims["height"]))
            btn.update_font(self.dims["font_size"], None)
        
        self.settings_button.update_dims(Dims(self.dims["x"], self.dims["y"] + (len(self.game_buttons) * (self.dims["height"] + self.dims["padding"])),\
                self.dims["width"], self.dims["height"]))
        self.quit_button.update_dims(Dims(self.dims["x"], self.dims["y"] + ((len(self.game_buttons) + 1) * (self.dims["height"] + self.dims["padding"])),\
                self.dims["width"], self.dims["height"]))
        
        
    
    def update(self, mouse, click = "None"):
        # Return False if no button is clicked
        # Return button that is clicked if a button is clicked
        # If click == "None", check for hover
        # If click == "Down", check for press
        # If click == "Up", check for release
            # If release is on a button, return that button
        # Draw all buttons
        # check press
        # check hover
        # check release
        res = self.check_mouse(mouse, click)
        self.draw()
        
        return res
    
    def draw(self):
        # Draw Background
        self.screen.fill(self.def_background_col)
        # Draw all buttons
        for btn in self.game_buttons:
            btn.draw(self.screen)
        self.settings_button.draw(self.screen)
        self.quit_button.draw(self.screen)
        pygame.display.flip()
        
        
        
    
    def check_mouse(self, mouse, click):
        # Check for collisions
        # If a collision occurs, it wont check for any other collisions
        # If a collision occurs, check what the current mouse state is (hover, press, release)
            # If hover, change the hover state of the button
            # If press, change the press state of the button
            # If release, return the button that was released
        res = None
        for btn in self.game_buttons:
            res = self.check_collision(btn, mouse, click)
            if res == True:
                return btn.text
        res = self.check_collision(self.settings_button, mouse, click)
        if res == True:
            return "Settings"
        res = self.check_collision(self.quit_button, mouse, click)
        if res == True:
            return "Quit"
        return None
    
    def check_collision(self, btn, mouse, click):
        if btn.check_click(mouse.x, mouse.y):
            if click == "Down":
                # Pressed
                btn.press()
            elif click == "Up":
                return True
            else:
                # Hovering
                btn.hover()
        else:
            btn.clear()
            
            
        
        
    
    
    def changeBGColor(self, color):
        self.def_background_col = color
    
    def changeBtnColor(self, color):
        self.def_button_col = color
        for btn in self.game_buttons:
            btn.change_bg_color(color)
        self.settings_button.change_bg_color(color)
        self.quit_button.change_bg_color(color)
    
    def changeTextColor(self, color):
        self.def_text_col = color
        for btn in self.game_buttons:
            btn.change_text_color(color)
        self.settings_button.change_text_color(color)
        self.quit_button.change_text_color(color)
        
    def changeFont(self, font):
        for btn in self.game_buttons:
            btn.change_font(font)
        self.settings_button.change_font(font)
        self.quit_button.change_font(font)
            
    # Instead of having check functions for press, hover, and release, maybe have a check function that looks for collision with a button, and then reacts based on if it was a hover, press, or release event
        
