
'''
~~~~ ui.py ~~~~

Contains all UI classes and elements for the pygame window:

Button:
    takes an image (in form of pygame.image) and dimensions (in form of misc.Dims) as inputs
    draws the button on the screen
    checks if the button is clicked




'''

import pygame # type: ignore
from pygame.locals import * # type: ignore


# Button Class
class Button:
    # Pygame Button
    def __init__(self, image, dims = None):
        # Requres dims to be the dims misc class
        # Pass it through into button to not need to import it into this file
        self.dims = dims
        if dims is None:
            raise ValueError("Dimensions must be provided")
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
    
class Text():
    def __init__(self, dims, text, color, bg_color, font):
        self.text = text
        self.font = font
        self.color = color
        self.bg_color = bg_color
        self.dims = dims
    
    def update_text(self, text):
        self.text = text
    
    def draw(self, screen):
        text = self.font.render(self.text, True, self.color)
        screen.blit(text, (self.dims.x, self.dims.y))
    
    def update_dims(self, dims):
        self.dims.x = dims.x
        self.dims.y = dims.y
        self.dims.width = dims.width
        self.dims.height = dims.height








if __name__ == "__main__":
    raise Exception("This file is not meant to be ran directly!")