# Pytext
Pytext is a open source text editor made in Python and it is inspired by the Vim editor. It has its own keybindings and uses Customtkinter to its interface. 
The project is in development and may not work correctly in MacOS. Feel free to open an issue to report bugs or share new ideas.

## Installation (Windows)
- run `git clone https://github.com/lorenzolpandolfo/pytext` inside your user's folder
- run `pip3 install -r requirements.txt` to install dependencies
- add the pytext directory to your user PATH variable

## Installation (Linux)
Make sure you installed the packages below:
- For Ubuntu/Debian based distros:
  `sudo apt install python3-tk python3-pil python3-pil.imagetk`
- For Archlinux based distros:
  `sudo pacman -S python-pillow`

Pytext installation process:
- run `git clone https://github.com/lorenzolpandolfo/pytext` inside your home folder
- run `pip3 install -r requirements.txt` to install Pytext's dependencies

## Preferences
- If you would like to change Pytext directory, don't forget to edit the `pytext.bat` (for Windows) or `pytext.sh` (for Linux) file after adding the custom directory to PATH.
- You can edit the `user/config.json` and `user/theme.json` files to change personal preferences.

## How to use
Pytext has two modes: **view** and **insert**.
In the view mode, you can navigate through the document and input keybinds.
And, in the insert mode, you can insert text to the file.
To switch from view mode to insert mode, just press i. And, to go to view mode, press Escape.

## Insert mode shortcuts:
Shortcut | Description
--- | --- 
Ctrl + z | undo
Ctrl + y | redo
Ctrl + x | cut the selected line(s)
Alt + up/down | move selected line(s) up/down
Alt + shift + up/down | clone selected line(s) up/down

## View mode keybinds:
You can add a number before the keybind to execute _n_ times. For example, the keybind `10W` will move the cursor up 10 lines.
Keybind | Description
--- | --- 
dd | delete line
WASD | move cursor
F/V | move to the first/last line
ww | save file
qq | quit without saving
wq | save and quit

