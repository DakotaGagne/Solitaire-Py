'''
~~~~ misc.py ~~~~

Contains all miscellaneous classes and elements for the game

Pos:
    helper class
    Ex - Card.pos.x
    Simply holds x and y values for a position

Dims:
    Holds x, y, width, and height values for a rectangle
    Used for buttons and other elements
    Ex - Button.dims.x



'''

import time

class Pos:
    # helper class
    # Ex - Card.pos.x
    def __init__(self, x = 0, y = 0):
        self.x = x
        self.y = y
        
class Dims:
    def __init__(self, x = 0, y = 0, width = 0, height = 0):
        self.x = x
        self.y = y
        self.width = width
        self.height = height


class Mouse:
    def __init__(self, dblClickDelay = 0.5):
        self.x = -1
        self.y = -1
        self.lastClick = time.time()
        self.dblClickDelay = dblClickDelay
        self.doubleClicked = False
        
    def check_double_click(self):
        self.doubleClicked = time.time() - self.lastClick < self.dblClickDelay
        self.lastClick = time.time()
        



if __name__ == "__main__":
    raise Exception("This file is not meant to be ran directly!")
