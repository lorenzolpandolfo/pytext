# Pytext
Pytext is a open-source Python text editor inspired by Vim, with its own keybindings, that uses Customtkinter to its interface. 
It's being developed on Windows and it may present instabilities on other operating systems. In future, It should support Linux and MacOS.
The project have a lot of progress to be made and it can be unstable with different screen resolutions too.
Feel free to open an issue or fork it!

Pytext code is under a total refactor process in the **unstable branch**. Use the main branch if you would like to run Pytext in its stablest version.

# Installation process - Windows
Pytext default directory is inside your user's folder. So, it is recommended that you clone the repository there.
To correctly install Pytext, follow these steps:
- run `git clone https://github.com/lorenzolpandolfo/pytext` inside your user's folder
- run `pip3 install -r requirements.txt` to install Pytext's dependencies
- (optional) add the Pytext's directory to your user PATH variable

If you add Pytext to PATH, you can launch it in terminal with `pytext <file_name>`. If the file doesn't exist, Pytext will create it.

# Installation process - Linux
- run `git clone https://github.com/lorenzolpandolfo/pytext` inside your home folder
- run `pip3 install -r requirements.txt` to install Pytext's dependencies

### Make sure you installed the packages below:

For Ubuntu/Debian based distros:
- `sudo apt install python3-tk python3-pil python3-pil.imagetk`

For Archlinux based distros:
- `sudo pacman -S python-pillow`

# Preferences
- If you would like to change Pytext directory, don't forget to edit the `pytext.bat` (for Windows) or `pytext.sh` (for Linux) file after adding the custom directory to PATH.
- You can edit the `user/config.json` and `user/theme.json` files to change some personal preferences.

# Use
To change from **view** to **insert** mode, you can use **Escape** or press the **i** key.

In the **view mode**, you can navigate through the document with arrow keys and use the keybinds after focusing the **command input text**, that is located on the right bottom corner.
To focus the command input text, you can use the **:** key or just press **Tab**.
In the **insert mode**, you can insert text to the current document and use **Ctrl** and **Alt** shortcuts, such as:
- **Ctrl + Z**: undo 
- **Ctrl + Y**: redo 
- **Ctrl + X**: cut a selected area or current line (cutting the current in progress)
- **Alt + Up or Down**: move a selected area or current line (in progress)
- **Alt + Shift + Up or Down**: copy and paste a selected area or current line (in progress)

# Current keybindings
You can add numbers after or before the keybind to run it more than one time. More keybinds will be added with time, as well as way to
remap them.
- **dd**: delete current line
- **WASD**: move through lines
- **ss**: save file
- **Q**: quit
- **sq, wq**: save and quit
- **O**: **On local directory**: List all files and folders in the current directory. You can select them with Return (enter) to navigate through directories and files
- **SO, so**: save and run On local directory command
- **nd** (**New Directory**): Creates a new directory in your local terminal directory
- **nf** (**New File**): Creates a new file in your local terminal directory
- **F**: move to the first line
- **V**: move to the last line

# Current TO-DO:
These features are not sure to be in the final version, but they look like a good idea at time. Features with ~strikethrough~ are already implemented or deprecated.
- Line counter modes:
  - ~number~
  - relativenumber
  - numberelative number
- A **keybinds.json** file to remap the standard Pytext keybinds.
- A keybind to select line(s)
- Add **CTRL +**
  - **X**: cut current line
  - **+** and **-**: change font size
  - **Enter**: if it is a script, run it
  - **S**: quick save file
- Add **Alt +**
  - **Arrow Keys**: move current line
  - **Shift + Arrow Keys**: copy and paste current line
- **Workplaces** from 1 to 10
- **Improve**
- - Ctrl + Arrow Keys movement
- - Better autocomplete text
- - **Tag optimization:** apply only to visible lines 
