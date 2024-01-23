import customtkinter as ctk
import os

class FontManager:
    @staticmethod
    def load_user_font(is_custom:bool = False, family:str = "", size:str = "", gui_size:str = "", title:str = "") -> int | tuple:
        if is_custom:
            FontManager.__move_to_fonts_directory__()

            if ".ttf" not in title:
                title = title + ".ttf"
            
            src = os.path.join(os.getcwd(), title)
            
            if not ctk.FontManager.load_font(src):
                return -1

        return (
            ctk.CTkFont(family=family, size=size),
            ctk.CTkFont(family=family, size=gui_size)
        )
    
    @staticmethod
    def __move_to_fonts_directory__():
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        os.chdir("..")
        os.chdir("fonts")