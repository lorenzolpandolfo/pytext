import customtkinter as ctk
from tkinterdnd2 import TkinterDnD

import sys
import os

from modules.commandManager import CommandManager
from modules.gui            import GUI
from modules.userConfig     import UserConfig
from modules.counter        import Counter
from modules.font           import Font
from modules.file           import File

class MainApp:
    def __init__(self, root, file_name = None):
        self.file_name = file_name
        self.root = root
        self.modo = "view"

        self.setup_instances()
        self.init_gui()
        self.init_command_manager()
        if self.file_name:
            self.File.open_local_directory_or_file(self.file_name, self.GUI.main_textarea, self, self.GUI, False, True)
        self.root.update()
        self.GUI.bottom_current_dir.configure(self.GUI.bottomframe, text="Welcome to The Pytext Editor!")
        self.Counter.atualizar_contador()

    def setup_instances(self):
        # loading instances from another classes
        self.File           = File(self.file_name, os.getcwd())
        self.UserConfig     = UserConfig(self)
        self.Font           = Font(self)
        self.Counter        = Counter(self)
        self.GUI            = GUI(self)
        self.CommandManager = CommandManager(self)

        self.Counter.gui = self.GUI


    def init_gui(self):
        self.GUI.setup(self.CommandManager, self.UserConfig)
        self.Font.start()
        self.GUI.start()


    def init_command_manager(self):
        self.CommandManager.setup(self.GUI, self.UserConfig, self.Counter)
        self.UserConfig.setup(self.GUI)
        self.CommandManager.capture_keybinds()


class Root(ctk.CTk, TkinterDnD.DnDWrapper):
    def __init__(self, *args, **kwargs):
        ctk.CTk.__init__(self, *args, **kwargs)
        self.TkdndVersion = TkinterDnD._require(self)


def check_if_filename():
    return len(sys.argv) > 1


if __name__ == "__main__":
    root = Root()
    if check_if_filename():
        app = MainApp(root, sys.argv[1])
    else: app = MainApp(root)
    root.mainloop()
