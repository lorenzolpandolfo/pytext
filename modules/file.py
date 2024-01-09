import os
import customtkinter as ctk

class File():
    def __init__(self, file_name, terminal_directory):
        self.current_directory = self.get_current_directory()
        self.file_name = file_name
        self.terminal_directory = terminal_directory
        print("TERMINALDIRECTORY: ", self.terminal_directory)

    def get_current_directory(self):
        return os.getcwd()
    
    def open_existent_file(self, file_name:str, textarea):
        full_path = os.path.join(self.terminal_directory, file_name)

        try:
            with open(full_path, "r+", encoding="utf8") as existent_file:
                textarea.configure(state="normal")
                content = existent_file.read()
                textarea.insert(ctk.END, content)
                textarea.configure(state="disabled")

        except FileNotFoundError: 
            return False