import os

import customtkinter as ctk
# import tkinter as tk
# from tklinenums import TkLineNumbers
from modules.tklinenums import TkLineNumbers

import pygments
from pygments.lexers import get_lexer_by_name
# from pygments.token import Token

from modules.UserConfig     import UserConfig
from modules.FontManager    import FontManager
from modules.ImageManager   import ImageManager
from modules.SyntaxColors   import SyntaxColors
from modules.FileManager    import FileManager


class MainApp(ctk.CTk):
    def __init__(self, terminal_dir:str, file_name:str):
        super().__init__()

        self.terminal_dir  = terminal_dir
        self.file_name     = file_name

        self.__load_user_config__()   
        self.__load_user_font__()
        self.__create_gui__()

        if self.file_name:
            print("ta tentando carregar o arquivo")
            self.__load_argv_file__()

    def __load_user_config__(self):
        self.config = UserConfig.get_user_config()
    
    def __load_user_font__(self):
        font = self.config["font"]

        loader = (
            FontManager.load_user_font(family=font["family"], size=font["size"], gui_size=font["gui_size"])
            if font["title"] == ""
            else FontManager.load_user_font(
                is_custom = True, title=font["title"], family=font["family"], size=font["size"], gui_size=font["gui_size"]
                ))
        
        if isinstance(loader, int):
            print(f"Error: could not load font '{font['title']}'. Loading default font instead.")
            self.font     = ctk.CTkFont("Consolas", 26)
            self.gui_font = ctk.CTkFont("Consolas", 17)
        else:
            self.font, self.gui_font = loader

    def __create_gui__(self):
        self.__create_window__()
        self.__configure_grids__()
        self.__create_frames__()
        self.__create_widgets__()

    def __create_widgets__(self):
        self.main_frame.create_textbox(font=self.font)
        self.main_frame.textbox.create_line_counter(self.left_frame)
        self.main_frame.textbox.set_tab_width(tabwidth=self.config["tab_width"])

        
        self.bottom_frame.create_widgets(output=(self.file_name if self.file_name else "Welcome to Pytext refactored"))
        self.bottom_frame.load_icons()


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

        self.main_frame = MainFrame(self)
        self.main_frame.grid(row=0, column=1, sticky="nsew")

        self.left_frame = LeftFrame(self)
        self.left_frame.grid(row=0, column=0, sticky="nsew")

    def __load_argv_file__(self):
        """Insert into main textbox the file that user specified as argv."""
        full_path = os.path.join(self.terminal_dir, file_name)
        content = FileManager.open_file(full_path)

        if content:
            self.main_frame.textbox.insert("1.0", content)
            self.main_frame.textbox.mark_set("insert", "1.0")


class LeftFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.__grid_setup__()
        self.configure(bg_color="#1D1E1E", fg_color="#1D1E1E")

    def __grid_setup__(self):
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
    

class BottomFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        
    def create_widgets(self, output:str):
        self.mode = ctk.CTkLabel(self, text="Insert", justify="center", font=self.master.gui_font)
        self.mode.grid(row=1, column=0)

        self.output = ctk.CTkLabel(self, text=output, padx=10, font=self.master.gui_font)
        self.output.grid(row=2, column=0)

    def load_icons(self):
        self.branch_image = ImageManager.get_image("branch", (22, 22))
    
    def create_branch_icon(self):
        self.branch = ctk.CTkLabel(self, image=self.branch_image, text="", justify="left")
        self.branch.grid(row=2, column=0)


class MainFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.__grid_setup__()

    def create_textbox(self, row:int = 0, column:int = 0, font:ctk.CTkFont | None = None):
        self.textbox = Texto(self, font=font)
        self.textbox.grid(row=row, column=column, sticky="nsew")
        self.textbox.configure(bg_color="#1D1E1E")
        self.master.update()
        self.textbox.focus_set()

    def __grid_setup__(self):
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)


class Texto(ctk.CTkTextbox):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self._lexer = pygments.lexers.PythonLexer
        self._colors = SyntaxColors.get_syntax_colors()

    def create_line_counter(self, master):
        self.update()
        self._line_counter = TkLineNumbers(master, self, justify="right", colors=("#e3ba68", "#1D1E1E"),tilde="~", bd=0)
        self._line_counter.grid(row=0, column=0, sticky="nsew", pady=(6,0))
        self.__enable_auto_redraw__()

    def __enable_auto_redraw__(self):
        self.bind("<Key>", lambda e: self.after_idle(self._line_counter.redraw), add=True)
        # self.bind("<KeyRelease>", lambda e: self.highlight_line())
        # self.bind("<Control-v>", lambda e: self.highlight_all())
        # self.bind("<Prior>", lambda e: self.highlight_all())

        # this yscrollcommand also auto resizes pytext to the current resolution
        self.configure(yscrollcommand=self.__y_scroll_command__)
    
    def __y_scroll_command__(self, *scroll_pos:tuple):
        self._y_scrollbar.set(scroll_pos[0], scroll_pos[1])
        self._line_counter.redraw()

    def set_tab_width(self, tabwidth:int):
        self.configure(tabs=self.cget("font").measure(" ") * tabwidth)

    def highlight_line(self, lexer="python", line_num:str=""):
        line_num = int(self.index("insert").split(".")[0]) if line_num == "" else line_num

        #for tag in self.tag_names(index=None):
        #    if tag.startswith("Token"):
        #        self.tag_remove(tag, "1.0", "end")
        #        self.tag_delete(tag)
        #        print(tag, " removida")
                
        lexer = get_lexer_by_name(lexer)
        content = self.get(f"{line_num}.0 linestart", f"{line_num}.0 lineend")
        tokens = list(pygments.lex(content, lexer))
        
        for tag in self.tag_names("insert"):
            if tag != "sel":
                # print(tag)
                self.tag_remove(tag, "insert linestart", "insert lineend")

        start_col = 0
        for (token, text) in tokens:
            token = str(token)

            end_col = start_col + len(text)
            if token not in ["Token.Text.Whitespace", "Token.Text"]:
                self.tag_add(token, f"{line_num}.{start_col}", f"{line_num}.{end_col}")
                #print(f"{line_num}.{start_col}", f"{line_num}.{end_col}")
                if token.split(".")[1] in self._colors:
                    self.tag_config(token, foreground=self._colors[token.split(".")[1]])
            start_col = end_col

        self.update()
        all = self.get("1.0", "end")
        num_lines = all.count("\n")
        
        first_line = int(self.index("@0,0").split(".")[0])
        last_line = int(
            self.index(f"@0,{self.winfo_height()}").split(".")[0]
        )

        for i in range(first_line, last_line):
            self.highlight_line("python", i)


if __name__ == "__main__":
    import sys
    file_name = sys.argv[1] if len(sys.argv) > 1 else ""
    if_argv_is_file = os.path.isfile(os.path.join(os.getcwd(), file_name))
    app = MainApp(terminal_dir=os.getcwd(), file_name=file_name) if if_argv_is_file else MainApp(terminal_dir=os.getcwd(), file_name="")
    app.mainloop()
