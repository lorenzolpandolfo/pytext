import customtkinter as ctk

class Font:
    def __init__(self):
        self.font = self.init_font()
        self.size = self.size()

    def init_font(self):
        src = r"fonts\firacode.ttf"
        # carrega a fonte
        ctk.FontManager.load_font(src)
        # agora ele reconhece a family Fira Code, porque eu carreguei antes
        return ctk.CTkFont(family="Fira Code", size=19)
    
    def size(self):
        return self.font.metrics()['linespace']