import customtkinter as ctk

class Font:
    def __init__(self, mainApp):
        self.main_app_instance = mainApp

    def start(self):
        self.font = self.init_font()
        self.size = self.size()


    def init_font(self):
        font = self.main_app_instance.UserConfig.font

        font_file_name = font["file_name"]
        font_family    = font["family"]
        font_size      = font["size"]

        # getting the font directory    
        src = r"fonts\{}.ttf".format(font_file_name)

        # load font
        ctk.FontManager.load_font(src)

        # now that i loaded the font, the family is recognized
        return ctk.CTkFont(family=f"{font_family}", size=font_size)
    
    def size(self):
        return self.font.metrics()['linespace']