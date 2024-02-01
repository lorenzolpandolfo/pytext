import customtkinter as ctk
import os
from modules.FileManager import FileManager as fm

class FontManager:
    @staticmethod
    def load_user_font(user_config_font:str) -> int | tuple:
        title = user_config_font["title"]

        if title:
            fm.move_to_directory("fonts")
            src = os.path.join(os.getcwd(), title)
            print(src)
            if not ctk.FontManager.load_font(src):
                return -1
        
        family    = user_config_font["family"]
        size      = user_config_font["size"]
        gui_size  = user_config_font["gui_size"]
        
        return (
            ctk.CTkFont(family=family, size=size),
            ctk.CTkFont(family=family, size=gui_size)
        )