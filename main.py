import customtkinter as ctk

from modules.commandManager import CommandManager
from modules.GUI import GUI
from modules.userConfig import UserConfig
from modules.counter import Counter
from modules.font import Font


class MainApp:
    def __init__(self, root):
        self.root = root
        self.modo = "view"

        self.setup_instances()
        self.init_gui()
        self.init_command_manager()


    def setup_instances(self):
        # loading instances from another classes
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
    

if __name__ == "__main__":
    root = ctk.CTk()
    app = MainApp(root)
    root.mainloop()
