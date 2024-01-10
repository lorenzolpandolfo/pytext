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
        print("abrindo", full_path)
        try:
            with open(full_path, "r+", encoding="utf8") as existent_file:
                textarea.configure(state="normal")
                content = existent_file.read()
                textarea.insert(ctk.END, content)
                textarea.configure(state="disabled")

        except FileNotFoundError: return False
    

    def open_local_directory_or_file(self, dir_name:str, textbox, mainapp, gui, updir = False):
        # if it is a valid directory 
        fulldir = os.path.join(self.terminal_directory, dir_name)
        fulldir_path_format = os.path.join(self.terminal_directory, dir_name[2:-1])
        print("abrindo ", fulldir)

        # if user is trying to open a directory
        if not updir:
            if os.path.isdir(fulldir_path_format):
                self.load_local_files_to_open(textbox, mainapp, path_to_open=fulldir_path_format)

            # if user is trying to open a file
            elif os.path.isfile(fulldir):
                with open(fulldir, "r", encoding="utf8") as file:
                    content = file.read()
                return gui.write_another_file_content(content, auto_insert=True)
            else:
                print("nao é file nem dir. ", fulldir, fulldir_path_format)
        else:
            if os.path.isdir(fulldir):
                self.load_local_files_to_open(textbox, mainapp, path_to_open=fulldir)
            else:
                print("o updir não é reconhecido")


    def load_local_files_to_open(self, textbox, mainapp, path_to_open:str = ""):
        """Runs when user Open the current directory"""
        localdirpreset = os.path.join(os.getcwd(), ".temp", "__pytextLocaldir__.txt")
        
        # if you need to open a specific path
        if path_to_open == "":
            current_terminal_directory = mainapp.File.terminal_directory

        # in this case, opens the local terminal path
        else:
            current_terminal_directory = path_to_open
            self.terminal_directory = current_terminal_directory

        files_in_current_dir = os.listdir(current_terminal_directory)
        print(current_terminal_directory)

        with open(localdirpreset, "w", encoding="utf8") as localdirpreset:
            textbox.configure(state="normal")
            textbox.delete("1.0", "end")

            for i, file in enumerate(files_in_current_dir):
                if os.path.isdir(os.path.join(current_terminal_directory, file)):
                    textbox.insert(f"{i + 1}.0", f"▼ {file}/\n")
                else:
                    textbox.insert(f"{i + 1}.0", f"{file}\n")
            
            textbox.insert(f"1.0", f"{current_terminal_directory}\n")
            textbox.configure(state="disabled")
            mainapp.File.file_name = "__pytextLocaldir__"
        
    def get_up_directory(self):
        return os.path.dirname(self.terminal_directory)