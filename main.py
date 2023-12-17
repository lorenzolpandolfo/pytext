import tkinter as tk
from tkinter import font
import customtkinter as ctk


class MainApp:
    def __init__(self, root):
        self.root = root
        self.create_window()
        self.create_frames()
        self.create_widgets()


    def create_window(self):
        root.geometry("1100x780")
        self.root.title("The Pytext Editor")
    

    def create_frames(self):
        # creating left frame
        self.leftframe = ctk.CTkFrame(root)
        self.leftframe.grid(row=0, column=0, sticky="ns")
        # peso 0 para não expandir (janela)
        self.root.columnconfigure(0, weight=0)

        # creating the main frame
        self.mainframe = ctk.CTkFrame(root)
        self.mainframe.grid(row=0, column=1, sticky="nsew")
        # peso 1 para que ele expanda (janela)
        self.root.columnconfigure(1, weight=1)
        self.root.rowconfigure(0, weight=1)

        # creating bottom frame
        self.bottomframe = ctk.CTkFrame(root)
        self.bottomframe.grid(row=1, column=0, columnspan=2, sticky="ew")


    def create_widgets(self):
        # initializing firacode font
        src = r"fonts\firacode.ttf"
        # carrega a fonte
        ctk.FontManager.load_font(src)
        # agora ele reconhece a family Fira Code, porque eu carreguei antes
        firacode = ctk.CTkFont(family="Fira Code", size=19) 

        # initializing main text area
        self.main_textarea = ctk.CTkTextbox(self.mainframe, wrap=ctk.WORD, font=firacode)
        self.main_textarea.grid(row=0, column=0, sticky="nsew", padx=10, pady=(20, 10))
        # configurando o mainframe
        self.mainframe.columnconfigure(0, weight=1)
        self.mainframe.rowconfigure(0, weight=1)

        # initializing left text area
        self.left_textarea = ctk.CTkTextbox(self.leftframe, width=50, wrap=ctk.CHAR, font=firacode)
        self.left_textarea.grid(row=0, column=0, sticky="ns", padx=(10,10), pady=(20,10))
        # configurando o leftframe
        self.leftframe.columnconfigure(0, weight=1)
        self.leftframe.rowconfigure(0, weight=1)

        # creating the bottom label
        bottom_output_mode = ctk.CTkLabel(self.bottomframe, text="view mode", justify="center", font=firacode)
        bottom_output_mode.grid(row=1, column=0, sticky="ew")
        # configurando o bottomframe
        self.bottomframe.columnconfigure(0, weight=1)
        self.bottomframe.rowconfigure(0, weight=1)

    
    

if __name__ == "__main__":
    root = ctk.CTk()
    app = MainApp(root)
    root.mainloop()