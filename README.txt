

'''
ISSUES / ADDITIONS
Issues:

# Make auto move function prioritize moving to a pile over an empty spot (iterate piles first then empty spaces)
        Want to make auto_move move to the largest pile first, and empty pile from left to right last




# Need to update each files comment section (top explainey part)
# Fix camelCase and other_case naming conventions
# Set a min width and height to make sure game looks correct
# Height of window needs to be proportionate to the width (16:9 or 4:3)
# Maybe add back the delay on the double click feature, make it like 1 or 2 sec


# Waste card stuck face down near end of game - In this case it was a 3 of clubs - Seems to be an issue with the visibility of the waste pile - Attempted a fix, doesnt seem to work - happens very rarely
        Likely fixed ^^^ - Fucking Nope (happens when I run out of the 3 cards and there is only one left in the pile, and none in the stock card)
        Also an issue where if there is one visible card left and I draw a stock card, it gets buried (only the first time)
        Waste card no longer stuck face down, but the issue still occurs. Also happened once in the middle of the waste pile with plenty of cards left  
            Somehow when a certain condition is met the card becomes unclickable - Idk what the specific condition is
    - Seems to be happening to tableau cards during Spider solitaire
    ******* Bug seems to be fixed for waste pile in klondike, still exists for Tableau most likely (not confirmed) ( maybe smth to do with undo)
        Have not noticed bug in either of the other two games


Additions:


# Spider Solitaire
    - Might want to add a way to communicate that I cant draw from stock when there is an empty pile
    - Might want to animate stock going to empty pile in some way
    - Maybe make a warning pop up on the bottom of the screen with the text relating to the issue


# Free Cell
    - Might want to add a way to communicate that I cant move more cards in a stack then there is room for in the free cells
    - Maybe make a warning pop up on the bottom of the screen with the text relating to the issue

# Tri Peaks Solitaire
# Add warning that pops up when a move is invalid (namely when drawing from stock pile in Spider, and a tableau has no cards, or when trying to move more cards than allowed in free cell)
    Text at the bottom of the screen, likely in red and bold, that pops up when an error is made, and goes away when the moves increase
    Could always draw it but empty the contents when moves increase, and add the text as needed throughout the code (likely in move card or click handler)

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