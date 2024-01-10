import os
import customtkinter as ctk

class File():
    def __init__(self, file_name, terminal_directory):
        self.current_directory = self.get_current_directory()
        self.file_name = file_name
        self.terminal_directory = terminal_directory


    def get_current_directory(self):
        return os.getcwd()
    

    def open_local_directory_or_file(self, dir_name:str, textbox, mainapp, gui, updir = False):
        """Runs when user try to open a file or directory inside the Open LocalDir"""
        fulldir = os.path.join(self.terminal_directory, dir_name)
        fulldir_path_format = os.path.join(self.terminal_directory, dir_name[2:-1])

        if not updir:
            # if user is trying to open a directory
            if os.path.isdir(fulldir_path_format):
                print(fulldir_path_format)
                self.load_local_files_to_open(textbox, mainapp, path_to_open=fulldir_path_format)

            # if user is trying to open a file
            elif os.path.isfile(fulldir):
                with open(fulldir, "r", encoding="utf8") as file:
                    content = file.read()
                return gui.write_another_file_content(content, file_name=dir_name, auto_insert=True)
            else:
                print("Path is not a file or a directory. ", fulldir, fulldir_path_format)
        
        # if user is trying to open a up directory
        else:
            if os.path.isdir(fulldir):
                self.load_local_files_to_open(textbox, mainapp, path_to_open=fulldir)
            else:
                print("Root directory not found: ", fulldir)


    def load_local_files_to_open(self, textbox, mainapp, path_to_open:str = ""):
        """Runs when user Open the current directory"""
        try:
            localdirpreset = os.path.join(os.getcwd(), ".temp", "__pytextLocaldir__.txt")
            
            # if you need to open a specific path
            if path_to_open == "":
                current_terminal_directory = mainapp.File.terminal_directory

            # in this case, opens the local terminal path
            else:
                current_terminal_directory = path_to_open

            files_in_current_dir = os.listdir(current_terminal_directory)

            with open(localdirpreset, "w", encoding="utf8") as localdirpreset:
                textbox.configure(state="normal")
                textbox.delete("1.0", "end")

                for i, file in enumerate(files_in_current_dir):
                    # if it is the last element
                    if i == len(files_in_current_dir) - 1:
                        # write in the file without the \n
                        if os.path.isdir(os.path.join(current_terminal_directory, file)):
                            textbox.insert(f"{i + 1}.0", f"▼ {file}/")
                        else:
                            textbox.insert(f"{i + 1}.0", f"{file}")
                    
                    else:
                        if os.path.isdir(os.path.join(current_terminal_directory, file)):
                            textbox.insert(f"{i + 1}.0", f"▼ {file}/\n")
                        else:
                            textbox.insert(f"{i + 1}.0", f"{file}\n")
                
                textbox.insert(f"1.0", f"{current_terminal_directory}\n")
                textbox.configure(state="disabled")
                mainapp.File.file_name = "__pytextLocaldir__"
                # Saving the current terminal directory after it sucessfully opens.
                self.terminal_directory = current_terminal_directory
        except PermissionError:
            print("Pytext doesn't have permission to open this file: ", path_to_open)

    def get_up_directory(self):
        return os.path.dirname(self.terminal_directory)