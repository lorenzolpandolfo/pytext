import customtkinter as ctk
import tkinter as tk
from tklinenums import TkLineNumbers

import pygments
from pygments.lexers import get_lexer_by_name
from pygments.token import Token


from modules.UserConfig     import UserConfig
from modules.SyntaxColors   import SyntaxColors
from modules.FontManager    import FontManager


class MainApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.__load_user_config__()   
        self.__load_user_font__()
        self.__create_gui__()


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
            print(f"Error: could not load font '{font["title"]}'. Loading default font instead.")
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
        self.main_frame.__create_textbox__(font=self.font)
        self.main_frame.textbox.__create_line_counter__(self.left_frame)

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


class LeftFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.configure(bg_color="#1D1E1E", fg_color="#1D1E1E")
    

class BottomFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.mode = ctk.CTkLabel(self, text="Insert", justify="center", font=master.gui_font)
        self.mode.grid(row=1, column=0)

        self.output = ctk.CTkLabel(self, text="Welcome to Pytext refactored", padx=10, font=master.gui_font)
        self.output.grid(row=2, column=0)


class MainFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)


    def __create_textbox__(self, row:int = 0, column:int = 0, font:ctk.CTkFont | None = None):
        # self.update()
        self.textbox = Texto(self, font=font)
        self.textbox.grid(row=row, column=column, sticky="nsew")
        self.textbox.configure(bg_color="#1D1E1E")
        self.master.update()
        self.textbox.focus_set()


class Texto(ctk.CTkTextbox):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self._lexer = pygments.lexers.PythonLexer
        self._colors = SyntaxColors.get_syntax_colors()

    def __create_line_counter__(self, master):
        self.update()
        self._line_counter = TkLineNumbers(master, self, justify="right", colors=("#e3ba68", "#1D1E1E"),tilde="~", bd=0)
        self._line_counter.grid(row=0, column=0, sticky="nsew", pady=(6,0))
        self.__enable_auto_redraw__()

    def __enable_auto_redraw__(self):
        self.bind("<Key>", lambda e: self.after_idle(self._line_counter.redraw), add=True)
        #self.bind("<KeyRelease>", lambda e: self.highlight_line())
        #self.bind("<Control-v>", lambda e: self.highlight_all())
        #self.bind("<Prior>", lambda e: self.highlight_all())

        # this yscrollcommand also auto resizes pytext to the current resolution
        self.configure(yscrollcommand=self.__y_scroll_command__)
    
    def __y_scroll_command__(self, *scroll_pos:tuple):
        self._y_scrollbar.set(scroll_pos[0], scroll_pos[1])
        self._line_counter.redraw()


    def highlight_line(self, lexer="python", line_num:str=""):
        if line_num == "": line_num = int(self.index("insert").split(".")[0])

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


    def highlight_all(self, lexer="python"):
        self.update()
        all = self.get("1.0", "end")
        num_lines = all.count("\n")
        
        first_line = int(self.index("@0,0").split(".")[0])
        last_line = int(
            self.index(f"@0,{self.winfo_height()}").split(".")[0]
        )

        for i in range(first_line, last_line):
            self.highlight_line("python", i)
        return 
        #for tag in self.tag_names(index=None):
        #    if tag.startswith("Token"):
        #        self.tag_remove(tag, "1.0", "end")
        #        self.tag_delete(tag)
        #        print(tag, " removida")
                
        lexer = get_lexer_by_name(lexer)
        content = self.get(f"1.0", f"end")
        tokens = list(pygments.lex(content, lexer))
        
        content = content.split("\n")

        start_col = 0
        for (token, text) in tokens:
            token = str(token)
            print(token, text)

            
            end_col = start_col + len(text)
            if token not in ["Token.Text.Whitespace", "Token.Text"]:
                for i, linha in enumerate(content):
                    if text in linha:
                        line_num = i + 1

                print(line_num)
                self.tag_add(token, f"{line_num}.{start_col}", f"{line_num}.{end_col}")
                print(f"{line_num}.{start_col}", f"{line_num}.{end_col}")
                if token.split(".")[1] in a:
                    self.tag_config(token, foreground=a[token.split(".")[1]])
            start_col = end_col


    def _setup_tags(self):
        for key in self.tag_names():
            print(key)
            self.tag_config(f"{key}", foreground="#1c92ba")

    
if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
