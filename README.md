# 2048 Drop

2048 Drop is a fast-paced, speed-play oriented fan remake of the Coolmath Games title [Number Drop](https://www.coolmathgames.com/0-number-drop), where two all-time classic puzzle games combine, Tetris and 2048.

Drop tiles next to tiles of the same value and they will merge into a higher value tile, freeing up space to drop more tiles and increase your score.

## Instructions

Use `←` and `→` to position the active tile.

Use `SPACE` to hard drop the tile.

Use the `Q W E SPACE I O P` keys to speed drop into one of the 7 columns instantly (if the tile can still make it there).

Use `ESC` to pause/unpause.

Use `R` to reset when the game is paused or stopped.

## Installation

Clone the repo and if you are using an M1/M2 based Mac simply run the `.app` file in `dist`. Otherwise see below for source building instructions.

### Building using pyinstaller

Install pyinstaller using pip

```shell
pip install -U pyinstaller
```

cd into the cloned directory and run the following:

#### MacOS

```shell
pyinstaller main.py -F -w -i 2048drop_icon.icns
```

#### Windows (untested)

```shell
pyinstaller main.py -F -w -i 2048drop_icon_64.ico
```

### Running using Python

Alternativley, just run `main.py` like any other python script. Ensure the following are available and installed:

-   pygame
-   numpy
