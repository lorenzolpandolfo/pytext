import tkinter as tk
import customtkinter as ctk
import re
import random

from modules import commandManager, GUI, userConfig, counter, font


class MainApp:
    def __init__(self, root):
        self.root = root
        self.modo = "view"
        self.Font = font.Font()
        self.Counter = counter.Counter(self)

        self.setup_instances()
        self.init_gui()
        self.init_command_manager()


    def setup_instances(self):
        # carregando as instancias das outras classes
        self.gui = GUI.GUI(self)
        self.command_manager = commandManager.CommandManager(self)
        self.user_config = userConfig.UserConfig(self.root)

        self.Counter.gui = self.gui

        # carregando configurações do usuário
        self.user_config.load_user_config()

        # enviando para as outras classes a sua instancia
        self.gui.main_app_instance = self
        self.command_manager.main_app_instance = self
        self.user_config.main_app_instance = self
        
        
    
    def init_gui(self):
        # inicia a criação da GUI
        self.gui.start()

        # envia para GUI a instancia do command_manager
        self.gui.setup(self.command_manager, self.user_config)


    def init_command_manager(self):
        # envia instancias para o command_manager
        self.command_manager.setup(self.gui, self.user_config, self.Counter)

        # carregando configurações do usuário
        self.user_config.setup(self.gui)

        # inicia a função de capturar keybinds
        self.command_manager.capture_keybinds()
    


if __name__ == "__main__":
    root = ctk.CTk()
    app = MainApp(root)
    root.mainloop()
