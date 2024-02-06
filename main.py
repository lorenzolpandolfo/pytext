import os

import customtkinter as ctk

from modules.UserConfig     import UserConfig
from modules.FontManager    import FontManager
from modules.FileManager    import FileManager
from modules.ThemeManager   import ThemeManager

from modules.frames.frames import MainFrame, LeftFrame, BottomFrame



class MainApp(ctk.CTk):
    def __init__(self, terminal_dir:str, file_name:str):
        super().__init__()

        self.terminal_dir  = terminal_dir
        self.file_name     = file_name
        self.theme_mode = self._get_appearance_mode()

        self.__load_user_config__()   
        self.__load_user_font__()
        self.__load_user_theme__()
        self.__create_gui__()

        if self.file_name:
            self.__load_argv_file__()
        self.__enable_binds__()

      
    def __load_user_config__(self):
        self.config = UserConfig.get_user_config()
    
    def __load_user_font__(self):
        font = self.config["font"]
        loader = FontManager.load_user_font(font)
        
        if isinstance(loader, int):
            print(f"Error: could not load font '{font['title']}'. Loading default font instead.")
            self.font     = ctk.CTkFont("Consolas", 26)
            self.gui_font = ctk.CTkFont("Consolas", 17)
        else:
            self.font, self.gui_font = loader

    def __load_user_theme__(self):
        self.theme = ThemeManager.get_user_theme()


    def __create_gui__(self):
        self.__create_window__()
        self.__configure_grids__()
        self.__create_frames__()
        self.__create_widgets__()

    def __create_window__(self):
        self.title("The Pytext Editor Refactored")
        self.geometry(self.config["window_size"])
        self.resizable(True, True)

    def __configure_grids__(self):
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)

        self.grid_columnconfigure(0, weight=0, minsize=60)
        self.grid_columnconfigure(1, weight=1)

    def __create_frames__(self):
        self.bottom_frame = BottomFrame(self)
        self.bottom_frame.grid(row=1, column=0, sticky="we", columnspan=2, rowspan=2)

        self.main_frame = MainFrame(self, self.font)
        self.main_frame.grid(row=0, column=1, sticky="nsew")

        self.left_frame = LeftFrame(self, self.font)
        self.left_frame.grid(row=0, column=0, sticky="nsew")
        
    def __create_widgets__(self):
        self.main_frame.create_textbox()
        self.main_frame.textbox.create_line_counter(self.left_frame)
        self.main_frame.textbox.set_tab_width(tabwidth=self.config["tab_width"])

        self.left_frame.create_textbox()
        
        self.bottom_frame.create_widgets(output=(self.file_name if self.file_name else "Welcome to Pytext refactored"))
        self.bottom_frame.load_icons()


    def __load_argv_file__(self):
        full_path = os.path.join(self.terminal_dir, self.file_name)

        self.main_frame.textbox.open_file(full_path)

        if FileManager.check_if_repository(full_path):
            self.bottom_frame.create_branch_icon(FileManager.get_git_branch(full_path))
        # else:
        #     self.bottom_frame.destroy_branch_icon()


    def __enable_binds__(self):
        self.bind("<Key>", lambda e: self.bind_dealing(e))
    
    def bind_dealing(self, event = None):
        # TODO - separar essa grande função em funções menores
        focus = str(self.focus_get())
        left_textbox_visible = self.left_frame.textbox.winfo_ismapped()
        print(event)

        if left_textbox_visible:
            if event.keysym == "Return":
                file_name = self.left_frame.textbox.get_current_line_content().strip()
                if file_name[0] == "▼":
                    self.left_frame.textbox.updir()
                    return self.left_frame.textbox.open_directory(self.left_frame.textbox.path)
                
                elif file_name[0] == "/":
                    file_name = file_name[1:]

                content = os.path.join(self.left_frame.textbox.path, file_name)

                if os.path.isdir(content):
                    return self.left_frame.textbox.open_directory(content)
                else:
                    # contar quantos diretorios tem antes e ir salvando a posicao do cursor pra retomar
                    if self.main_frame.textbox.open_file(content):
                        self.main_frame.textbox.focus_set()

            

        if event.keysym == "Escape" and left_textbox_visible:
            self.left_frame.hide_textbox()
            self.main_frame.textbox.focus_set()
        
        elif (event.state & 0x4) and event.keysym == "f":
            if left_textbox_visible:
                if "leftframe" in focus:
                    self.left_frame.hide_textbox()
                    self.main_frame.textbox.focus_set()
                else:
                    self.left_frame.textbox.focus_set()
            else:
                self.left_frame.show_textbox()
                self.left_frame.textbox.focus_set()
        
        else:
            cur_text = self.bottom_frame.command.cget("text")
            if event.char.isalpha() or event.char.isdigit():
                self.bottom_frame.command.configure(text=cur_text + event.char)



if __name__ == "__main__":
    import sys
    file_name = sys.argv[1] if len(sys.argv) > 1 else ""
    # check if this is not problematic. I think that it is not
    file_name = file_name[2:] if file_name[:2] == ".\\" else file_name
    if_argv_is_file = os.path.isfile(os.path.join(os.getcwd(), file_name))
    app = MainApp(terminal_dir=os.getcwd(), file_name=file_name) if if_argv_is_file else MainApp(terminal_dir=os.getcwd(), file_name="")
    app.mainloop()
