import os
import customtkinter as ctk
from time import sleep

class File():
    def __init__(self, file_name, terminal_directory):
        self.current_directory = self.get_current_directory()
        self.file_name = file_name
        self.terminal_directory = terminal_directory
        self.setup_files_to_not_show_in_gui()
        self.pos_per_dir = []



    def setup_files_to_not_show_in_gui(self):
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        os.chdir("..")
        os.chdir(os.path.join(os.curdir, ".temp"))
        self.files_to_not_show_in_gui = [file[:-4] for file in os.listdir()]


    def get_current_directory(self):
        return os.getcwd()
    

    def open_local_directory_or_file(self, dir_name:str, textbox, mainapp, gui, updir = False):
        """Runs when user try to open a file or directory inside the Open LocalDir"""
        fulldir = os.path.join(self.terminal_directory, dir_name)
        fulldir_path_format = os.path.join(self.terminal_directory, dir_name[2:-1])

        # if user is trying to open a up directory (..)
        if updir:
            if os.path.isdir(fulldir):
                return self.load_local_files_to_open(textbox, mainapp, path_to_open=fulldir)
            # else: print("Root directory not found: ", fulldir)

        # if user is trying to open a directory
        if os.path.isdir(fulldir_path_format):
            return self.load_local_files_to_open(textbox, mainapp, path_to_open=fulldir_path_format, cursor_pos=textbox.index(ctk.INSERT))

        # if user is trying to open a file
        elif os.path.isfile(fulldir):
            with open(fulldir, "r", encoding="utf8") as file:
                try: content = file.read()
                except UnicodeDecodeError: return gui.bottom_output_detail.configure(text=f"Invalid file extension ({dir_name})")
            return gui.write_another_file_content(content, file_name=dir_name, auto_insert=True)
        else:
            return gui.bottom_output_detail.configure(text="Path is not a file or a directory")
            # print("Path is not a file or a directory. ", fulldir, fulldir_path_format)
        

    def load_local_files_to_open(self, textbox, mainapp, path_to_open:str = "", cursor_pos = "2.0"):
        """Runs when user Opens the current directory"""
        try:
            # path_to_open is used to open a custom path
            current_terminal_directory = self.terminal_directory if path_to_open == "" else path_to_open
            files_in_current_dir = os.listdir(current_terminal_directory)
            
            componentes_caminho = os.path.normpath(current_terminal_directory).split(os.path.sep)
            upper_dir_count = len(componentes_caminho) - 1

            textbox.configure(state="normal")
            textbox.delete("1.0", "end")
            all_tags = []
        
            for i, file in enumerate(files_in_current_dir):
                cur_line = int(textbox.index(ctk.INSERT).split(".")[0])

                # check if its the last element. True if i = len(files_in_current_dir) - 1
                is_last_element = i == len(files_in_current_dir) - 1

                # check if it is a directory
                is_dir = os.path.isdir(os.path.join(current_terminal_directory, file))

                file_type_prefix = "▼ " if is_dir else ""
                file_type_sufix = "/" if is_dir else ""

                textbox.insert(f"{i + 1}.0", f"{file_type_prefix}{file}{file_type_sufix}" + ("" if is_last_element else "\n"))
                
                tag_name = f"dir_color{i}" if is_dir else f"file_color{i}"
                textbox.tag_add(tag_name, f"{cur_line}.0", f"{cur_line}.end")
                all_tags.append(tag_name)

            for tag in all_tags:
                color = mainapp.UserConfig.theme["file_color"] if "file" in tag else mainapp.UserConfig.theme["dir_color"]
                textbox.tag_config(tag, foreground=color)

            # insert the current terminal directory in the first line
            textbox.insert(f"1.0", f"{current_terminal_directory}\n")
            textbox.tag_add("curdir", "1.0", "1.end")
            textbox.tag_config("curdir", foreground="green")

            textbox.configure(state="disabled")
            mainapp.File.file_name = "__pytextLocaldir__"
            # Saving the current terminal directory after it sucessfully opens
            self.terminal_directory = current_terminal_directory

            # adding dirs last mouse pos (2.0 default)
            if self.pos_per_dir == []:
                for i in range(upper_dir_count):
                    self.pos_per_dir.append("2.0")
                    textbox.mark_set(ctk.INSERT, "2.0")
                    textbox.see("2.0")
                    
            else:
                # if user go to a updir 
                if len(self.pos_per_dir) > upper_dir_count:
                    textbox.mark_set(ctk.INSERT, self.pos_per_dir[-1])
                    textbox.see(f"{self.pos_per_dir[-1]}")
                    self.pos_per_dir.pop()
                    mainapp.GUI.mover_tela(move_to_center=True)

                # if user go to an inside dir
                elif len(self.pos_per_dir) < upper_dir_count:
                    self.pos_per_dir.append(cursor_pos)
                    textbox.mark_set(ctk.INSERT, "2.0")
                    textbox.see("2.0")
                    
            mainapp.GUI.realcar_linha_selecionada()
            mainapp.GUI.bottom_current_dir.configure(text=self.get_formatted_to_gui_cur_dir(self.terminal_directory, self.file_name))
            mainapp.Counter.atualizar_contador()

        except PermissionError:
            return mainapp.GUI.bottom_output_detail.configure(text="Pytext doesn't have permission to open this file")
            # print("Pytext doesn't have permission to open this file: ", path_to_open)
        


    def get_up_directory(self):
        return os.path.dirname(self.terminal_directory)


    def create_new_file(self, gui):
        self.file_name = None
        return gui.write_another_file_content("", file_name=None, auto_insert=True)


    def create_new_directory(self, dir_name:str, textbox, mainapp):
        full_path = os.path.join(self.terminal_directory, dir_name)
        if not os.path.exists(full_path):
            os.makedirs(full_path)
        self.load_local_files_to_open(textbox, mainapp, path_to_open=self.terminal_directory)
    

    def insert_new_dir_title(self, gui):
        newDirTitlepreset = os.path.join(os.getcwd(), "pytext", ".temp", "__pytextNewDirTitle__.txt")

        with open(newDirTitlepreset, "r", encoding="utf8") as file:
            content = file.read()
            gui.write_another_file_content(content, True)
            self.file_name = "__pytextNewDirTitle__"


    def get_formatted_to_gui_cur_dir(self, curdir:str, curfile:str):
        """ Format correctly to gui the current directory and file """
        if curfile in self.files_to_not_show_in_gui:
            curfile = ""

        formatted_to_gui:str = curdir + f" ({curfile})" if curfile else curdir
        return formatted_to_gui.replace("\\","/")