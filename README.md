# Pytext
Pytext is a open-source Python text editor that uses Customtkinter to its interface. 
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