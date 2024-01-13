import customtkinter as ctk
import os

class Font:
    def __init__(self, mainApp):
        self.main_app_instance = mainApp

    def start(self):
        self.font = self.init_font()
        self.gui_font = self.init_font(gui_font=True)
        self.size = self.size()
        #print(self.font["family"], self.gui_font["family"])
        

    def init_font(self, gui_font = False):
        font = self.main_app_instance.UserConfig.font
        #if font["absolute_font"]:
        #    return ctk.CTkFont(font["absolute_font"][0], 16) if gui_font else ctk.CTkFont(font["absolute_font"][0], 25)

        font_file_name = font["file_name"]
        font_family    = font["family"]
        font_size      = font["gui_size"] if gui_font else font["size"]

        if font["file_name"] != "":
            # getting the font directory
            src = r"fonts\{}.ttf".format(font_file_name)
            os.chdir("..")
            # load font
            ctk.FontManager.load_font(src)
            print("Custom font loaded: ", src)

        # now that i loaded the font, the family is recognized
        return ctk.CTkFont(font_family, font_size)
    
    def size(self):
        return self.font.metrics()['linespace']