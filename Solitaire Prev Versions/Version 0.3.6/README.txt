

'''
ISSUES / ADDITIONS
Issues:
# Waste card stuck face down near end of game - In this case it was a 3 of clubs - Seems to be an issue with the visibility of the waste pile - Attempted a fix, doesnt seem to work - happens very rarely
        Likely fixed ^^^ - Fucking Nope (happens when I run out of the 3 cards and there is only one left in the pile, and none in the stock card)
        Also an issue where if there is one visible card left and I draw a stock card, it gets buried (only the first time)
        Waste card no longer stuck face down, but the issue still occurs. Also happened once in the middle of the waste pile with plenty of cards left  
            Somehow when a certain condition is met the card becomes unclickable - Idk what the specific condition is
# Height of window needs to be proportionate to the width (16:9 or 4:3)
# Set a min width and height to make sure game looks correct    
# Lower the max height of the tableau pile
# Fix camelCase and other_case naming conventions



Additions:

# Spider Solitaire
    10 Tableau Piles - D
    3 Modes - One Suit, Two Suit, Four Suit - D
    Can stack cards in descending order on tableau, with the same suit existing
        Will need to check if a K-A pile exists in tableau - Move to foundation if so
    8 Foundation Piles - Only gets filled if there is a pile in the tableau from K-A same suit - D
    104 cards total (2 of each)
    Starting state:
        4 Left Tableaus - 5 Face down cards, one face up
        6 Right Tableaus - 4 cards face down, one face up
    Stock Pile:
        Will add one card face up to the bottom of each pile in the tableau
    
    Changes to code:
        Will need to rebuild from the klondike class to make the spider class
        Make Spider Deck instead of Klondike deck (Same except the generation)
            Will need to generate deck based on the game type (1,2,4 suit)
            One suit - Spades only
            Two suit - Spades and Hearts
        Tableau pile will stay basically the same, since there is 10 piles though, might affect the way "clicked" works
            Right now the format is T15 
                "T" for tableau
                "1" for pile pos
                "5" for pile pos
                Could either do 0-9 for tableau (will likely work)
                Or need a check to determine if the number is one or two digits
            Tableau Will also need a check for a completed stack
            Also add a function that removes the completed stack from the tableau
                Set the top most card face up as well
            Any card can go onto an empty tableau slot
            Tableau will also need a function that takes a list of cards and adds one to each tableau face up
        Stock:
            Will need to have a function that pulls the number of cards needed to add one to each tableau pile
            All tableau piles must have at least one card to draw from stock pile
        Foundation:
            King to Ace (Ace on top)
        

# Hint Feature (unsure how to implement yet)
    2 Ideas:
        1. Find all possible moves and using a priority system, suggest move to best spot
        2. Suggest first possible move found or stock pile click if no moves found
    Could alternatively just make a help button that performs a move for the player, without suggesting it first
# Need an always winable variable and feature 
    Can either generate a random deck, and have an ai play it to completion, and add it to a json or similar file that can store the start state of the winnable games
    Or can have an algorithm that reverses the game from the end state to the start state and uses that (would not have to store it in a JSON)
    May not need to use a storage feature either way
# Buttons to go from main menu to settings to game, and vice versa

# Optional auto complete feature (show button if available) when tableau only contains 4 full stacks ( might be able to if tableau[0] is king and stock / waste is empty) - 
           Maybe make it a toggle that allows for auto movement to foundation at all times (would naturally auto complete at end of game but player can choose to enable it earlier)
            DONE - Auto complete is mandatory currently
# Add a settings menu
# Add a pause menu
# Add a Game win / Game Loss Overlay (Built into gamerenderer)

# Save and Load Game feature (should tie into the undo feature)

# Display time elapsed - Partial; Font Issues, want m:s time
# Display number of moves - Partial; Font Issues

# Free Cell
# Tri Peaks Solitaire


'''





'''
===MENU PLANS===
Main Loop:
    Should be able to tell what menu we are in or if we are in game window
    Maybe have a bool variable for each menu
    if Main Menu is True then draw the main menu and use it as focus
    if Settings Menu is True then draw the settings menu and use it as focus
    if Pause Menu is True then draw the pause menu and use it as focus
        if Pause Menu is True we ovveride the game window
    if Any one of the three is True, the others should be false
    if none are true, then we are in the game windo

Main Menu:
    Buttons for each game
    Settings Button
    Quit Button
    When a button is clicked, the game mode is set to the game that was clicked
    Until a button is clicked, the game mode is None
    



Settings Menu
    Unsure what settings there should be yet
    Probably good idea to have the card images, background color, etc
    Audio settings if sound gets added
    Back Button to Main Menu (or maybe back to pause menu if in game)    

Pause Menu
    Resume Button
    Main Menu Button
    Settings Button
    Save Button
    Load Button
    Quit Button


Game Window
    Overarching window that contains the game
    Will draw the screen needed depending on where we are
    Will have the game loop
'''