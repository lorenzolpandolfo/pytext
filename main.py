import tkinter as tk
import customtkinter as ctk
import random

class MainApp:
    def __init__(self, root):
        self.root = root
        self.window()
        self.create_frames()
        self.create_widgets()
        self.bind()


    def resize(self, w):
        self.mainframe.configure(width = w)
        self.root.update()

    def bind(self):
        # Com essa função, eu consigo realizar uma ação por movimento da janela, resize, alt+tab nela, etc
        # <Configure> é mudanças na janela. <Button-1> seria o mouse1, por exemplo
        # Sem o lambda e, ele não roda a função varias vezes
        root.bind("<Configure>", lambda : self.resize())

    def window(self):
        root.geometry("740x780")
        self.root.title("Pytext")
    

    def create_frames(self):
        self.mainframe = ctk.CTkFrame(root, width=100)
        self.mainframe.pack(expand=True)


    def create_widgets(self):
        self.textarea = ctk.CTkTextbox(self.mainframe, width=90, height=90)
        self.textarea.pack(expand=True, padx=10, pady=(20,10))
    
    


if __name__ == "__main__":
    root = ctk.CTk()
    app = MainApp(root)
    root.mainloop()
