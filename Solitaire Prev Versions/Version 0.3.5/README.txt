

'''
ISSUES / ADDITIONS
Issues:
# Waste card stuck face down near end of game - In this case it was a 3 of clubs - Seems to be an issue with the visibility of the waste pile - Attempted a fix, doesnt seem to work - happens very rarely
        Likely fixed ^^^ - Fucking Nope (happens when I run out of the 3 cards and there is only one left in the pile, and none in the stock card)
        Also an issue where if there is one visible card left and I draw a stock card, it gets buried (only the first time)
# Height of window needs to be proportionate to the width
# Set a min width and height to make sure game looks correct    
# Lower the max height of the tableau pile


# Error notes: - Should be fixed
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

# Drag feature
    Maybe have a clicked trigger that is true if a click occurs and selected card is none, and is false if click is released and selected card is not none
    In this case we set the selected card to the card that was clicked on and if the card is released, keep it highlighted but disable the drag feature
    In draw - if card is selected and mouse click down is true, draw that card at the mouse position (or cards if its a tableau stack)
    Idea:
    I changed the mouse click detection to be true and false depending on if it was clicked or not
    As it sits:
        All "clicks" occur when pressed was True in the last frame and False in the current
        Every detection for cards being clicked occurs here
    What if I changed it so that when the prev state was False, and the current is True, AND no card is selected, perform the card selection
    What I could do then is make it so that if the click is still held, draw the selected card(s) to be centered on the mouse (more like upper middle)
    When the click is then released, that is when I can check if the mouse is colliding with another card
        If it is not, or the move is illegal, the card simply stays selected and gets drawn in its normal position
    Concern:
        How to tell when I should be treating the selection as a "drag" and when I should default to the standard movement
    Challenge:
        Want to make it change as little in the code as possible
    If I use a variable in the game class called dragging, and set it to true when the mouse is depressed, false when it is unpressed,
    I should be able to do it
    If dragging is False, buisness as usual (in the click checker / handler, check for a mouse click and a selection on one of the cards)
        If the mouse is depressed, and colliding with a card, check if a card is already selected. If it is, attempt to make the move.
        If no card is currently selected, select the card, and set dragging to True
    Draw function should not have to change
    Card positioning function should
        If a card is selected, next check if dragging is True, if so set the position of the card (and all others below the selected card)
        to be centered on the mouse. If not, draw it to where it should go
    Click handling conditions:
        Card coll, selected False, dragging False - select card and dragging = True
        Card coll, selected True, dragging True (click False) - Attempt the move
            If the move fails, card stays selected, dragging = False
            If the move succeeds, normal conditions occur, dragging = False
        Card coll, selected True, dragging False, click True - Normal move state (note that releasing the click no longer counts as a move)
        No card coll, selected True, dragging True - Selection remains True, Dragging becomes False
    Technically the states passed to the class is "Up" "Down" and "None"
        When the mouse is first pressed down, "Down" is passed
        When the mouse is first released, "Up" is passed
        "None" is passed if the state is the same as the previous frame
    With that in mind, the biggest change is that "Down" becomes the heavy lifter
        It is used to set selections, make moves when dragging = False, etc
    "Up" is used only if selected and dragging are True
    
    
    
                    Click handler should remain the same, until a collision is detected
                        Then the first check should be if click is "Up" or "Down"
                        "Up"
                            Should check if dragging and selected are True
                                ***Stopping case for if the collided card is the same as the original card 
                                                                (dragging set to False, nothing else changes)
                                If so the move should be Attempted
                                    If the move succeeds, great
                                    If it fails, then selected should become false, and dragging should be set to False
                                If not, do nothing
                        "Down"
                            Check if selected = True
                                If so:
                                    ***check if dragging is False (if not raise error as it should be False)
                                    Attempt Move
                                        Success - great
                                        Fail - selected = False
                                If not:
                                    Select card (if legal)
                                    Set dragging to True
                        **Note: I was wrong above
                            If I set the position of the card to the mouse, then the click detection would always find 
                                                                                                            the same card
                            Instead I must change Draw to ignore the position of the card when drawing and instead 
                                                                                                        center on mouse there
                            This way the "pos" of the card never changes, all collision detection remains accurate








# Optional auto complete feature (show button if available) when tableau only contains 4 full stacks ( might be able to if tableau[0] is king and stock / waste is empty) - 
           Maybe make it a toggle that allows for auto movement to foundation at all times (would naturally auto complete at end of game but player can choose to enable it earlier)
            DONE - Auto complete is mandatory currently
# Add a settings menu
# Add a pause menu
# Add a Game win / Game Loss Overlay (Built into gamerenderer)
# Spider Solitaire

# Save and Load Game feature (should tie into the undo feature)

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