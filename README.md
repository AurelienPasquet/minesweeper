# Minesweeper Game

This is a classic Minesweeper game developed using Python and Pygame, allowing customizable grid dimensions and bomb count.

## Requirements

    Python 3.x
    Pygame library

To install Pygame, use:
```bash
pip install pygame
```

## Installation

Clone or download this repository.

```bash
git clone https://github.com/AurelienPasquet/minesweeper.git
# or
git clone git@github.com:AurelienPasquet/minesweeper.git
```

## Running the Game

Enter the game reposirory:

```bash
cd minesweeper
```

Run the main file with optional arguments for grid size and bomb count:

```bash
python src/main.py <width> <height> [num_bombs]
```
- **width** - Number of tiles along the horizontal axis (default: 30).
- **height** - Number of tiles along the vertical axis (default: 16).
- **num_bombs** - Total bombs on the grid (default: 99).

## Example:

```bash
python src/main.py 10 10 20
```

## Additional Controls

- **q** - Quit the game.
- **r** - Restart the game.

## Credits

The sprites used in this project were created by [RockPaperKatana](https://www.spriters-resource.com/submitter/RockPaperKatana/). The sheet can be found [here](https://www.spriters-resource.com/custom_edited/minesweepercustoms/sheet/180218/).
