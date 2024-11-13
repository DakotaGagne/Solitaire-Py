'''
~~~~ definitions.py ~~~~

Contains global defs for game

Variables:
    CARD_PATHS_CLASSIC - paths for classic card deck (in pygame.image format)
    CARD_PATHS_MODERN - paths for modern card deck (in pygame.image format)
    BUTTON_PATHS - paths for buttons (in pygame.image format)



'''



import pygame # type: ignore




CARD_PATHS_CLASSIC = {
  "back": pygame.image.load("assets/Deck_Sprites/Backs/Card-Back-05.png"),
  
  "01C": pygame.image.load("assets/Deck_Sprites/Cards/Classic/c01.png"),
  "02C": pygame.image.load("assets/Deck_Sprites/Cards/Classic/c02.png"),
  "03C": pygame.image.load("assets/Deck_Sprites/Cards/Classic/c03.png"),
  "04C": pygame.image.load("assets/Deck_Sprites/Cards/Classic/c04.png"),
  "05C": pygame.image.load("assets/Deck_Sprites/Cards/Classic/c05.png"),
  "06C": pygame.image.load("assets/Deck_Sprites/Cards/Classic/c06.png"),
  "07C": pygame.image.load("assets/Deck_Sprites/Cards/Classic/c07.png"),
  "08C": pygame.image.load("assets/Deck_Sprites/Cards/Classic/c08.png"),
  "09C": pygame.image.load("assets/Deck_Sprites/Cards/Classic/c09.png"),
  "10C": pygame.image.load("assets/Deck_Sprites/Cards/Classic/c10.png"),
  "11C": pygame.image.load("assets/Deck_Sprites/Cards/Classic/c11.png"),
  "12C": pygame.image.load("assets/Deck_Sprites/Cards/Classic/c12.png"),
  "13C": pygame.image.load("assets/Deck_Sprites/Cards/Classic/c13.png"),
  
  "01D": pygame.image.load("assets/Deck_Sprites/Cards/Classic/d01.png"),
  "02D": pygame.image.load("assets/Deck_Sprites/Cards/Classic/d02.png"),
  "03D": pygame.image.load("assets/Deck_Sprites/Cards/Classic/d03.png"),
  "04D": pygame.image.load("assets/Deck_Sprites/Cards/Classic/d04.png"),
  "05D": pygame.image.load("assets/Deck_Sprites/Cards/Classic/d05.png"),
  "06D": pygame.image.load("assets/Deck_Sprites/Cards/Classic/d06.png"),
  "07D": pygame.image.load("assets/Deck_Sprites/Cards/Classic/d07.png"),
  "08D": pygame.image.load("assets/Deck_Sprites/Cards/Classic/d08.png"),
  "09D": pygame.image.load("assets/Deck_Sprites/Cards/Classic/d09.png"),
  "10D": pygame.image.load("assets/Deck_Sprites/Cards/Classic/d10.png"),
  "11D": pygame.image.load("assets/Deck_Sprites/Cards/Classic/d11.png"),
  "12D": pygame.image.load("assets/Deck_Sprites/Cards/Classic/d12.png"),
  "13D": pygame.image.load("assets/Deck_Sprites/Cards/Classic/d13.png"),

  "01H": pygame.image.load("assets/Deck_Sprites/Cards/Classic/h01.png"),
  "02H": pygame.image.load("assets/Deck_Sprites/Cards/Classic/h02.png"),
  "03H": pygame.image.load("assets/Deck_Sprites/Cards/Classic/h03.png"),
  "04H": pygame.image.load("assets/Deck_Sprites/Cards/Classic/h04.png"),
  "05H": pygame.image.load("assets/Deck_Sprites/Cards/Classic/h05.png"),
  "06H": pygame.image.load("assets/Deck_Sprites/Cards/Classic/h06.png"),
  "07H": pygame.image.load("assets/Deck_Sprites/Cards/Classic/h07.png"),
  "08H": pygame.image.load("assets/Deck_Sprites/Cards/Classic/h08.png"),
  "09H": pygame.image.load("assets/Deck_Sprites/Cards/Classic/h09.png"),
  "10H": pygame.image.load("assets/Deck_Sprites/Cards/Classic/h10.png"),
  "11H": pygame.image.load("assets/Deck_Sprites/Cards/Classic/h11.png"),
  "12H": pygame.image.load("assets/Deck_Sprites/Cards/Classic/h12.png"),
  "13H": pygame.image.load("assets/Deck_Sprites/Cards/Classic/h13.png"),

  "01S": pygame.image.load("assets/Deck_Sprites/Cards/Classic/s01.png"),
  "02S": pygame.image.load("assets/Deck_Sprites/Cards/Classic/s02.png"),
  "03S": pygame.image.load("assets/Deck_Sprites/Cards/Classic/s03.png"),
  "04S": pygame.image.load("assets/Deck_Sprites/Cards/Classic/s04.png"),
  "05S": pygame.image.load("assets/Deck_Sprites/Cards/Classic/s05.png"),
  "06S": pygame.image.load("assets/Deck_Sprites/Cards/Classic/s06.png"),
  "07S": pygame.image.load("assets/Deck_Sprites/Cards/Classic/s07.png"),
  "08S": pygame.image.load("assets/Deck_Sprites/Cards/Classic/s08.png"),
  "09S": pygame.image.load("assets/Deck_Sprites/Cards/Classic/s09.png"),
  "10S": pygame.image.load("assets/Deck_Sprites/Cards/Classic/s10.png"),
  "11S": pygame.image.load("assets/Deck_Sprites/Cards/Classic/s11.png"),
  "12S": pygame.image.load("assets/Deck_Sprites/Cards/Classic/s12.png"),
  "13S": pygame.image.load("assets/Deck_Sprites/Cards/Classic/s13.png")

}

CARD_PATHS_MODERN = {
  "back": pygame.image.load("assets/Deck_Sprites/Backs/Card-Back-05.png"),
  
  "01C": pygame.image.load("assets/Deck_Sprites/Cards/Modern/c01.png"),
  "02C": pygame.image.load("assets/Deck_Sprites/Cards/Modern/c02.png"),
  "03C": pygame.image.load("assets/Deck_Sprites/Cards/Modern/c03.png"),
  "04C": pygame.image.load("assets/Deck_Sprites/Cards/Modern/c04.png"),
  "05C": pygame.image.load("assets/Deck_Sprites/Cards/Modern/c05.png"),
  "06C": pygame.image.load("assets/Deck_Sprites/Cards/Modern/c06.png"),
  "07C": pygame.image.load("assets/Deck_Sprites/Cards/Modern/c07.png"),
  "08C": pygame.image.load("assets/Deck_Sprites/Cards/Modern/c08.png"),
  "09C": pygame.image.load("assets/Deck_Sprites/Cards/Modern/c09.png"),
  "10C": pygame.image.load("assets/Deck_Sprites/Cards/Modern/c10.png"),
  "11C": pygame.image.load("assets/Deck_Sprites/Cards/Modern/c11.png"),
  "12C": pygame.image.load("assets/Deck_Sprites/Cards/Modern/c12.png"),
  "13C": pygame.image.load("assets/Deck_Sprites/Cards/Modern/c13.png"),
  
  "01D": pygame.image.load("assets/Deck_Sprites/Cards/Modern/d01.png"),
  "02D": pygame.image.load("assets/Deck_Sprites/Cards/Modern/d02.png"),
  "03D": pygame.image.load("assets/Deck_Sprites/Cards/Modern/d03.png"),
  "04D": pygame.image.load("assets/Deck_Sprites/Cards/Modern/d04.png"),
  "05D": pygame.image.load("assets/Deck_Sprites/Cards/Modern/d05.png"),
  "06D": pygame.image.load("assets/Deck_Sprites/Cards/Modern/d06.png"),
  "07D": pygame.image.load("assets/Deck_Sprites/Cards/Modern/d07.png"),
  "08D": pygame.image.load("assets/Deck_Sprites/Cards/Modern/d08.png"),
  "09D": pygame.image.load("assets/Deck_Sprites/Cards/Modern/d09.png"),
  "10D": pygame.image.load("assets/Deck_Sprites/Cards/Modern/d10.png"),
  "11D": pygame.image.load("assets/Deck_Sprites/Cards/Modern/d11.png"),
  "12D": pygame.image.load("assets/Deck_Sprites/Cards/Modern/d12.png"),
  "13D": pygame.image.load("assets/Deck_Sprites/Cards/Modern/d13.png"),
  
  "01H": pygame.image.load("assets/Deck_Sprites/Cards/Modern/h01.png"),
  "02H": pygame.image.load("assets/Deck_Sprites/Cards/Modern/h02.png"),
  "03H": pygame.image.load("assets/Deck_Sprites/Cards/Modern/h03.png"),
  "04H": pygame.image.load("assets/Deck_Sprites/Cards/Modern/h04.png"),
  "05H": pygame.image.load("assets/Deck_Sprites/Cards/Modern/h05.png"),
  "06H": pygame.image.load("assets/Deck_Sprites/Cards/Modern/h06.png"),
  "07H": pygame.image.load("assets/Deck_Sprites/Cards/Modern/h07.png"),
  "08H": pygame.image.load("assets/Deck_Sprites/Cards/Modern/h08.png"),
  "09H": pygame.image.load("assets/Deck_Sprites/Cards/Modern/h09.png"),
  "10H": pygame.image.load("assets/Deck_Sprites/Cards/Modern/h10.png"),
  "11H": pygame.image.load("assets/Deck_Sprites/Cards/Modern/h11.png"),
  "12H": pygame.image.load("assets/Deck_Sprites/Cards/Modern/h12.png"),
  "13H": pygame.image.load("assets/Deck_Sprites/Cards/Modern/h13.png"),
  
  "01S": pygame.image.load("assets/Deck_Sprites/Cards/Modern/s01.png"),
  "02S": pygame.image.load("assets/Deck_Sprites/Cards/Modern/s02.png"),
  "03S": pygame.image.load("assets/Deck_Sprites/Cards/Modern/s03.png"),
  "04S": pygame.image.load("assets/Deck_Sprites/Cards/Modern/s04.png"),
  "05S": pygame.image.load("assets/Deck_Sprites/Cards/Modern/s05.png"),
  "06S": pygame.image.load("assets/Deck_Sprites/Cards/Modern/s06.png"),
  "07S": pygame.image.load("assets/Deck_Sprites/Cards/Modern/s07.png"),
  "08S": pygame.image.load("assets/Deck_Sprites/Cards/Modern/s08.png"),
  "09S": pygame.image.load("assets/Deck_Sprites/Cards/Modern/s09.png"),
  "10S": pygame.image.load("assets/Deck_Sprites/Cards/Modern/s10.png"),
  "11S": pygame.image.load("assets/Deck_Sprites/Cards/Modern/s11.png"),
  "12S": pygame.image.load("assets/Deck_Sprites/Cards/Modern/s12.png"),
  "13S": pygame.image.load("assets/Deck_Sprites/Cards/Modern/s13.png")
}


BUTTON_PATHS = {
  "undo": pygame.image.load("assets/Buttons/undo.png"),
  "blank": pygame.image.load("assets/Buttons/blank.png"),
  "pause": pygame.image.load("assets/Buttons/pause.png"),
  "resume": pygame.image.load("assets/Buttons/resume.png"),
  "quit": pygame.image.load("assets/Buttons/quit.png"),
  "exit_small": pygame.image.load("assets/Buttons/exit_small.png"),
  "settings": pygame.image.load("assets/Buttons/settings.png"),
  "settings_small": pygame.image.load("assets/Buttons/settings_small.png")
}