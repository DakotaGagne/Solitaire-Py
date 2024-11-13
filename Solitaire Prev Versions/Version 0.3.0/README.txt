

'''
ISSUES / ADDITIONS
Issues:
# Waste card stuck face down near end of game - In this case it was a 3 of clubs - Seems to be an issue with the visibility of the waste pile - Attempted a fix, doesnt seem to work - happens very rarely
# Undo is bugged again - If I undo and then repeat action, then undo again, it wont work - Rebuild undo feature properly
    Create a Backup and Restore function for each class up to klondike
# Height of window needs to be proportionate to the width
# Set a min width and height to make sure game looks correct    
# Will need to fix the GameRenderer so that it handles always having mouse pos, but takes optional click var as well like MenuRenderer
# Want to better implement the down and up click into the game - Namely so that the buttons remain large if down is held, without spamming the click if up is occuring
        Idea - use pygame.key.get_pressed() and find the mouse key in it. If mouse 1 is pressed, override the current state of click variable in main.py

# Error notes:
            Number of cards to fetch is 0
            ERROR!!!! Card is None after fetching!!!!
            [K of Hearts, Q of Clubs, J of Hearts, 10 of Spades]
            ColIdx: 1
            CardIdx: 1
    I think that there may be somewhere that double fetches a card?
    Seems to happen when I double click (albiet rare) - Maybe in auto_move function?
    Moved from 2nd col to 3rd col - there was a 2 of diamonds in the 2nd col that the king was below
    The empty image for the first col dissapeared as well
    Auto move should have moved the card stack to the first col not the third col
    Stack move behaves correctly when there is no card above the king

Additions:


# Main Menu
    Simple menu with buttons for each game, settings, and quit
    Settings menu should have options for card back, card front, background color, and maybe a few other things
    Quit should just quit the game
    Game buttons should take you to the gam
    Buttons should have hover effects
    Buttons should have a click effect
    Maintain window size when entering the game
    game variable is the game that was chosen in the main menu
    use same loop to handle all menus, just change the renderer


# Add a settings menu
# Spider Solitaire

# Optional auto complete feature (show button if available) when tableau only contains 4 full stacks ( might be able to check if tableau[0] is king and stock / waste is empty) - 
           Maybe make it a toggle that allows for auto movement to foundation at all times (would naturally auto complete at end of game but player can choose to enable it earlier)
# Save and Load Game feature (should tie into the undo feature)
# Drag feature
    Maybe have a clicked trigger that is true if a click occurs and selected card is none, and is false if click is released and selected card is not none
    In this case we set the selected card to the card that was clicked on and if the card is released, keep it highlighted but disable the drag feature
    In draw - if card is selected and mouse click down is true, draw that card at the mouse position (or cards if its a tableau stack)

# Display time elapsed - Partial; Font Issues, want m:s time
# Display number of moves - Partial; Font Issues
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
    if none are true, then we are in the game window
    Pseudo Code:
        if Main Menu:
            Draw Main Menu
            if Klondike Button Clicked:
                Main Menu = False
                Game Window = True
                Game Mode = Klondike
            if Spider Button Clicked:
                Main Menu = False
                Game Window = True
                Game Mode = Spider
            if FreeCell Button Clicked:
                Main Menu = False
                Game Window = True
                Game Mode = FreeCell
            if Settings Button Clicked:
                Main Menu = False
                Settings Menu = True
            if Quit Button Clicked:
                Quit Game
        if Settings Menu:
            Draw Settings Menu
            if Back Button Clicked:
                Settings Menu = False
                Main Menu = True
        if Pause Menu:
            Draw Pause Menu
            if Resume Button Clicked:
                Pause Menu = False
                Game Window = True
            if Main Menu Button Clicked:
                Pause Menu = False
                Main Menu = True
            if Settings Button Clicked:
                Pause Menu = False
                Settings Menu = True
            if Quit Button Clicked:
                Quit Game
        if Game Window:
            Draw Game Window
            if Pause Button Clicked:
                Game Window = False
                Pause Menu = True
            if Main Menu Button Clicked:
                Game Window = False
                Main Menu = True
            if Settings Button Clicked:
                Game Window = False
                Settings Menu = True
            if Quit Button Clicked:
                Quit Game

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