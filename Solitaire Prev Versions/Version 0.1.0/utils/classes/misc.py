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



class Pos:
    # helper class
    # Ex - Card.pos.x
    def __init__(self, x = None, y = None):
        self.x = x
        self.y = y
        
class Dims:
    def __init__(self, x = 0, y = 0, width = 0, height = 0):
        self.x = x
        self.y = y
        self.width = width
        self.height = height


if __name__ == "__main__":
    raise Exception("This file is not meant to be ran directly!")
