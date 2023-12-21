import tkinter as tk
import customtkinter as ctk
import re
import random

from modules import commandManager, GUI, userConfig



class MainApp:
    def __init__(self, root):
        self.root = root
        self.modo = "view"

        # carregando as instancias das outras classes 
        self.gui = GUI.GUI(self.root)
        self.command_manager = commandManager.CommandManager(self.root)
        self.user_config = userConfig.UserConfig(self.root)

        self.user_config.load_user_config()

        # enviando para as outras classes a sua instancia
        self.gui.main_app_instance = self
        self.command_manager.main_app_instance = self
        
        # inicia a criação da GUI
        self.gui.start()

        # envia para GUI a instancia do command_manager
        self.gui.setup(self, self.command_manager, self.user_config)
        # envia instancias para o command_manager
        self.command_manager.setup(self, self.gui.main_textarea, self.gui.bottom_command_output, self.gui, self.user_config)

        # inicia a função de capturar keybinds
        self.command_manager.capture_keybinds()


if __name__ == "__main__":
    root = ctk.CTk()
    app = MainApp(root)
    root.mainloop()
