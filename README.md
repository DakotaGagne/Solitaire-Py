# Solitaire-Py

Solitaire-Py is a Python-based implementation of classic solitaire games using the Pygame library. The project aims to provide a fully functional and visually appealing solitaire game with multiple game modes, including Klondike, Spider, and Freecell.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/DakotaGagne/Solitaire-Py.git
   ```
2. Navigate to the project directory:
   ```bash
   cd Solitaire-Py
   ```
3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

To start the game, run the `main.py` file:

```bash
python main.py
```

## Project Structure

### Main Files

- **main.py**: The entry point of the game. It initializes the game, sets up the display, and contains the main game loop.

### Renderer Files

- **MainMenuRenderer.py**: Contains the `MainMenuRenderer` class, which is used to render the main menu of the game.
- **SettingsMenuRenderer.py**: Contains the `SettingsMenuRenderer` class, which is used to render the settings menu.
- **PauseMenuRenderer.py**: Contains the `PauseMenuRenderer` class, which is used to render the pause menu.
- **GameRenderer.py**: Contains the `GameRenderer` class, which handles the rendering of the game itself.

### Game Logic Files

- **klondike.py**: Contains the `Klondike` class, which implements the rules and logic for the Klondike game mode.
- **spider.py**: Contains the `Spider` class, which implements the rules and logic for the Spider game mode.
- **freecell.py**: Contains the `Freecell` class, which implements the rules and logic for the Freecell game mode.

### Component Files

- **card.py**: Contains the `Card` class, which represents a single card in the game.
- **deck.py**: Contains the `Standard_Deck` and `Spider_Deck` classes, which represent the decks of cards used in the game.
- **tableau.py**: Contains the `Tableau` class, which represents the tableau piles in the game.
- **foundation.py**: Contains the `Foundation` class, which represents the foundation piles in the game.
- **stock.py**: Contains the `Stock` class, which represents the stock and waste piles in the game.
- **free_cell.py**: Contains the `Free_cell` class, which represents the free cells in the Freecell game mode.

### Utility Files

- **ui.py**: Contains the UI elements such as `ButtonImg` and `ButtonRect` classes for creating buttons.
- **misc.py**: Contains miscellaneous helper classes such as `Pos`, `Dims`, and `Mouse`.
- **definitions.py**: Contains global definitions and paths for game assets.

## In Progress

### Current Issues

- Auto move function needs to prioritize moving to a pile over an empty spot.
- Update each file's comment section for better documentation.
- Fix the issue where a card becomes unclickable under certain conditions in Spider solitaire.

### Planned Additions

- Improve Spider Solitaire by adding visual cues for invalid moves and animating stock to empty pile transitions.
- Enhance Freecell with additional features and improvements.
- Implement an optional auto-complete feature that can be toggled on or off.
- Add a settings menu for adjusting game preferences.
- Add a pause menu for pausing the game.
- Implement game win and game loss overlays.
- Add audio settings if sound is added to the game.
- Implement save and load game functionality.

## Acknowledgements

- Pygame library for providing the tools to create the game.

## Contributions

- Dakota Gagne - All of the programming for the game
