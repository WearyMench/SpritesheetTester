# Spritesheet Tools

Spritesheet Tools is a small Python + Pygame app for building and previewing sprite sheets. It provides a simple menu-driven workflow to:

- create a spritesheet from multiple images
- test an existing spritesheet with animation controls
- adjust the grid layout and playback settings in real time

## Features

### Creator mode

- combine several images into a single spritesheet
- automatically calculate a grid layout based on the number of frames
- manually override columns and rows if needed
- preview the spritesheet before saving it
- test the generated spritesheet directly from the same workflow

### Tester mode

- load a spritesheet from disk or use the built-in browse dialog
- preview the animation with adjustable speed
- adjust columns, rows, loop behavior, and frame position
- view the active frame and grid overlay for easier debugging

## Project structure

- `main.py` — launches the main menu and switches between creator and tester modes
- `spritesheet_creator.py` — combines images into a spritesheet
- `spritesheet_tester.py` — loads and animates a spritesheet
- `create_test_spritesheet.py` — helper script for generating a sample test sheet
- `requirements.txt` — Python dependencies

## Requirements

- Python 3.9+
- Pygame 2.5+

## Installation

1. Clone the repository
2. Open a terminal in the project folder
3. Create and activate a virtual environment if you want one
4. Install dependencies:

```bash
pip install -r requirements.txt
```

## Run the app

Start the project from the repository root:

```bash
python main.py
```

From the menu you can choose either:

- `Create Spritesheet`
- `Test Spritesheet`

## Controls

### Tester

- `SPACE` — play/pause animation
- `LEFT/RIGHT` — previous/next frame
- `Q/E` — decrease/increase columns
- `A/D` — decrease/increase rows
- `Z/C` — decrease/increase animation speed
- `L` — toggle loop mode
- `G` — toggle grid overlay
- `R` — reset frame
- `B` — browse for a spritesheet file
- `ESC` — quit

### Creator

- `B` — browse for images
- `G` — set custom grid size
- `S` — save the spritesheet
- `T` — test the spritesheet
- `C` — clear loaded images
- `ESC` — quit

## Notes

- The tester can automatically look for default filenames such as `spritesheet.png`, `sprite.png`, and `test.png` in the project folder.
- For best results, use images that are similar in size when generating a new spritesheet.
- This project is intended as a lightweight local tool rather than a packaged web app.
