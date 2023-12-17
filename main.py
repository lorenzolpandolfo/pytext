import tkinter as tk
import customtkinter as ctk
import random

class MainApp:
    def __init__(self, root):
        self.root = root
        self.create_window()
        self.create_frames()
        self.create_widgets()


    def create_window(self):
        root.geometry("740x780")
        self.root.title("The Pytext Editor")
    

    def create_frames(self):
        # creating the main frame
        self.mainframe = ctk.CTkFrame(root, width=100)
        self.mainframe.pack(expand=True, fill="both")

        # creating the left label
        teste = ctk.CTkLabel(self.mainframe, width=5)
        teste.pack(side=tk.LEFT, expand=False, fill='both')

    def create_widgets(self):
        self.textarea = ctk.CTkTextbox(self.mainframe, width=90, height=90, wrap=ctk.WORD)
        self.textarea.pack(expand=True, fill="both", padx=10, pady=(20,10))
    
    

if __name__ == "__main__":
    root = ctk.CTk()
    app = MainApp(root)
    root.mainloop()