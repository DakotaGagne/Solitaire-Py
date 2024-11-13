
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
from .misc import Dims

# Button Class

# Change this to ButtonImg class
class ButtonImg:
    # Pygame Button (Using Image)
    def __init__(self, image, dims, text_data = None):
        # Requres dims to be the dims misc class
        # Pass it through into button to not need to import it into this file
        
        self.image = image
        self.dims = dims
        if dims is None:
            raise ValueError("Dimensions must be provided")
        
        self.text = None
        self.text_color = None
        self.font = None
        
        if text_data is not None:
            if "text" in text_data:
                self.text = text_data["text"]
            else:
                raise ValueError("Text must be provided")
            if "text_color" in text_data:
                self.text_color = text_data["text_color"]
            else:
                self.text_color = (255, 255, 255)
            if "font" in text_data:
                self.font = text_data["font"]
            else:
                self.font = pygame.font.Font(None, 36) ############################## Need to make font sizeable with window

        self.hovering = False
        self.clicking = False
        
        
    
    def update_dims(self, dims):
        if type(dims) is dict:
            self.dims.x = dims["x"]
            self.dims.y = dims["y"]
            self.dims.width = dims["width"]
            self.dims.height = dims["height"]
        else:
            self.dims = dims
            
    def update_font(self, font_size, font_type = None):
        self.font = pygame.font.Font(font_type, font_size)
    
    
    
    def draw(self, screen):
        dims = None
        if self.clicking:
            dims = self.dims
            self.dims = Dims(self.dims.x, self.dims.y, self.dims.width * 1.05, self.dims.height * 1.05)
            self.dims.x -= (self.dims.width - dims.width) / 2
        
        self.image = pygame.transform.scale(self.image, (self.dims.width, self.dims.height))
        screen.blit(self.image, (self.dims.x, self.dims.y))
        
        if self.text is not None:
            text = self.font.render(self.text, True, self.text_color)
            screen.blit(text, (self.dims.x + self.dims.width / 2 - text.get_width() / 2, self.dims.y + self.dims.height / 2 - text.get_height() / 2))
        
        # If hovering or clicking, add a darker overlay
        if self.hovering:
            hover_overlay = pygame.Surface((self.dims.width, self.dims.height))
            hover_overlay.set_alpha(75)  # Transparency level
            hover_overlay.fill((0, 0, 0))  # Black overlay
            screen.blit(hover_overlay, (self.dims.x, self.dims.y))
            
        if dims is not None:
            self.dims = dims
        
    def check_click(self, x, y):
        if self.dims.x <= x <= self.dims.x + self.dims.width and self.dims.y <= y <= self.dims.y + self.dims.height:
            return True
        return False

    def press(self):
        self.clicking = True
        self.hovering = False
        
    def hover(self):
        self.hovering = True
        self.clicking = False
    
    def clear(self):
        self.hovering = False
        self.clicking = False
    
    
# Implement this!!
class ButtonRect():
    # Pygame Button (Using Rectangle)
    def __init__(self, text, dims, text_color, bg_color, font = None):
        # Requres dims to be the dims misc class
        # Pass it through into button to not need to import it into this file
        # Will probably need to make the font sizeable with the window like everything else
        
        self.text = text
        self.dims = dims
        self.text_color = text_color
        self.bg_color = bg_color
        self.font = font
        if self.font is None:
            self.font = pygame.font.Font(None, 36)
        if dims is None:
            raise ValueError("Dimensions must be provided")
        self.rect = pygame.Rect(dims.x, dims.y, dims.width, dims.height)
        self.hover = False
        self.click = False
    
    def update_dims(self, dims):
        if type(dims) is dict:
            self.dims.x = dims["x"]
            self.dims.y = dims["y"]
            self.dims.width = dims["width"]
            self.dims.height = dims["height"]
        else:
            self.dims = dims
        self.rect = pygame.Rect(dims.x, dims.y, dims.width, dims.height)
    
    def draw(self, screen):
        pygame.draw.rect(screen, self.bg_color, self.rect)
        text = self.font.render(self.text, True, self.text_color)
        screen.blit(text, (self.dims.x, self.dims.y))
        
    def check_click(self, x, y):
        if self.dims.x <= x <= self.dims.x + self.dims.width and self.dims.y <= y <= self.dims.y + self.dims.height:
            print("UNDO CLICKED")
            return True
        return False

    def change_text(self, text):
        self.text = text
    
    def change_bg_color(self, bg_color):
        self.bg_color = bg_color
        
    def change_text_color(self, text_color):
        self.text_color = text_color
        
    def change_font(self, font):
        self.font = font
    
    
    
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