# Pytext
Pytext is a open source text editor made in Python and it is inspired by the Vim editor. It has its own keybindings and uses tkinter to its interface.
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
- run `pip3 install -r requirements.txt` to install dependencies
- add the pytext directory to your user PATH variable

## Preferences
- You can edit the `user/config.json` and `user/theme.json` files to change personal preferences.

## How to use
After adding pytext directory to your PATH variable, you can use `pytext <file>` to open a file.
Pytext has two modes: **view** and **insert**.
In the view mode, you can navigate through the document and input keybinds.
And, in the insert mode, you can insert text to the file.
To switch from view mode to insert mode, just press i. And, to go to view mode, press Escape.

## Insert mode shortcuts:
Shortcut | Description
--- | --- 
Shift + : | focus file textbox
Ctrl + e | open/close file explorer
Ctrl + t | new tab
Ctrl + w | close current tab
Ctrl + tab | move to next tab
F2 (in file explorer) | rename file to
Ctrl + Return | new line above
Ctrl + F5 | run code
Ctrl + z / y | undo / redo
Ctrl + c / v | copy / paste
Ctrl + x | cut the selected line(s)
Ctrl + , | open config.json file
Ctrl + =/- | make font bigger/smaller
Alt + up / down | move selected line(s) up / down
Alt + shift + up / down | clone selected line(s) up / down

## View mode keybinds:
You can add a number before the keybind to execute _n_ times. For example, the keybind `10W` will move the cursor up 10 lines.
Keybind | Description
--- | --- 
dd | delete line
WASD | move cursor
F / V | move to the first / last line
ww | save file
qq | quit
wq | save and quit

