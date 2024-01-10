# Pytext
Pytext is a open-source Python text editor inspired in Vim, with its own keybindings, that uses Customtkinter to its interface. 
It's being developed on Windows and it may present instabilities on other operating systems. In future, It should support Linux and MacOS.
The project have a lot of progress to be made and it can be unstable with different screen resolutions too.
Feel free to open an issue or fork it!

# Installation process
Pytext default directory is inside your user's folder. So, it is recommended that you clone the repository there.
To correctly install Pytext, follow these steps:
- run `git clone https://github.com/lorenzolpandolfo/pytext` inside your user's folder
- run `pip install -r requeriments.txt` to install Pytext's dependencies
- (optional) add the Pytext's directory to your user PATH variable

If you add Pytext to PATH, you can launch it in terminal with `pytext <file_name>`. If the file doesn't exist, Pytext will create it.

# Preferences
- If you want to change Pytext directory, don't forget to edit the `pytext.bat` file after adding the custom directory to PATH.
- You can edit the `modules/config.json` file to change some personal preferences.

# Current keybindings
You can add numbers after or before the keybind to run it more than one time. More keybinds will be added with time, as well as way to
remap them.
- **dd**: delete current line
- **wasd**: move through lines
- **S**: save file
- **Q**: quit
- **O**: **Open**/**On local directory**: List all files and folders in the current directory. You can select them with Return (enter) to navigate through directories and files.
- **nd**: **New Directory**: Creates a new directory in your local terminal directory.
- **nf**: **New File**: Creates a new file in your local terminal directory.

# Current TO-DO:
These features are not sure to be in the final version, but they look like a good idea at time.
- New GUI improvements, showing the current directory and file title
- Line counter modes:
  - number
  - relativenumber
  - numberelative number
- A **keybinds.json** file to remap the standard Pytext keybinds.
- New keybindings, such as:
   - **gg**: move to the first absolute line
   - **bb**: move to the last absolute line
- Add **CTRL +**
  - **Z**: undo
  - **X**: cut current line
  - **+** and **-**: change font size
  - **Shift** + **N**: create a new file (maybe useless because of workspaces)
  - **Enter**: if it is a script, run it
- Add **Alt +**
  - **Arrow Keys**: move current line
  - **Shift + Arrow Keys**: copy and paste current line
- **Workplaces** from 1 to 10
- Colors to key words for each programming language. Make the colors custom too!
- Add a git support to check the repository info
