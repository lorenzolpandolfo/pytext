from customtkinter import CTkTextbox, CTkScrollbar
import os

from modules.FileManager    import FileManager
from modules.tklinenums     import TkLineNumbers
from modules.SyntaxColors   import SyntaxColors
from modules.Application    import Application

import pygments
from pygments.lexers import get_lexer_by_name


class Generaltext(CTkTextbox):
    """ Includes methods that Maintext and Lefttext use. """
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.selected_line_color = None
        self.path = None

        self.sys_theme = master.sys_theme
        self.theme = master.theme
        self.tab_width = Application.mainapp.config["tab_width"]

    def enable_auto_highlight_line(self):
        self.bind("<Key>", lambda _: self.after_idle(self.highlight_selected_line))
        self.bind("<Button-1>", lambda _: self.after_idle(self.highlight_selected_line))

    def highlight_selected_line(self, event=None):
        line_start = int(self.index("insert").split(".")[0])
        self.tag_remove("current_line_color", "1.0", "end")
        self.tag_add("current_line_color", f"{line_start}.0", f"{line_start + 1}.0")
        self.tag_config("current_line_color", background=self.selected_line_color)

    def load_theme(self, child):
        dark = "_dark" if self.sys_theme == "dark" else ""
        child = str(child)

        widget = "main_textbox" if "maintext" in child else "left_textbox"

        bg_color            = self.theme["widgets"][widget][f"bg{dark}"]
        selected_line_color = self.theme["widgets"][widget][f"selected_line{dark}"]
        font_color          = self.theme["widgets"][widget][f"font{dark}"]
        exp_dir_color       = self.theme["explorer"][f"dir{dark}"]
        exp_file_color      = self.theme["explorer"][f"file{dark}"]
        exp_curdir_color    = self.theme["explorer"][f"curdir{dark}"]

        return bg_color, selected_line_color, font_color, exp_dir_color, exp_file_color, exp_curdir_color

    def write_file_content(self, content: str | tuple, mark_set: str = "insert"):
        """ Directly write a file content. Used when user opens a file with left sidebar or argv"""
        if not content:
            content = ''
        self.configure(state="normal")

        self.delete("1.0", "end")
        self.insert("1.0", content)

        if mark_set:
            self.mark_set(mark_set, "1.0")
        
        if Application.get_mode() == "insert":
            Application.switch_mode()
        else:
            self.configure(state="disabled")

    def write_directory_content(self, content: tuple, colors: tuple, mark_set: str = "insert"):
        """ Write files from a directory. Deals with directories colors. """
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        self.configure(state="normal")

        raw_content = content[0]
        formatted_content = content[1]

        self.delete("1.0", "end")
        self.insert("1.0", formatted_content)
        
        # adding colors to other directories inside the content
        for i, file in enumerate(raw_content.split("\n")):
            full_path = os.path.join(self.path, file)

            if os.path.isdir(full_path):
                self.tag_add("directory_color", f"{i + 2}.0", f"{i + 3}.0")
                self.tag_config("directory_color", foreground=colors[0])
            
            elif os.path.isfile(full_path):
                self.tag_add("file_color", f"{i + 2}.0", f"{i + 3}.0")
                self.tag_config("file_color", foreground=colors[1])
            
        if mark_set:
            self.mark_set(mark_set, "1.0")
        
        self.configure(state="disabled")

    def open_file(self, full_path: str):
        """ Open a file through a directory and title. Then, write it. """
        content = FileManager.open_file(full_path)
        self.write_file_content(content)

        Application.set_current_file(full_path)
        return content

    def open_directory(self, dir_path: str, auto_write:bool = True):
        content = FileManager.open_directory(dir_path)
        if content:
            self.path = dir_path

            if auto_write:
                self.write_directory_content(content, colors=(self.exp_dir_color, self.exp_file_color, self.exp_curdir_color))

    def set_tab_width(self, tabwidth:int):
        self.configure(tabs=self.cget("font").measure(" ") * tabwidth)

    def focus_set(self):
        super().focus_set()
        self.highlight_selected_line()

    def get_current_line_content(self):
        line_start = int(self.index("insert").split(".")[0])
        return self.get(f"{line_start}.0", f"{line_start + 1}.0")


class Maintext(Generaltext):
    """Represents the main textbox of Pytext."""
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self._line_counter = None

        self.sys_theme = master.sys_theme
        self.theme = master.theme
        self.__load_theme__()

        super().enable_auto_highlight_line()

        self._lexer = pygments.lexers.PythonLexer
        self._colors = SyntaxColors.get_syntax_colors()
        self._enable_binds_()

    def __load_theme__(self):
        (self.bg_color, self.selected_line_color, self.font_color, self.exp_dir_color,
self.exp_file_color, self.exp_curdir_color) = super().load_theme(self)
        self.configure(bg_color=self.bg_color, fg_color=self.bg_color, text_color=self.font_color, state="disabled")

    def _enable_binds_(self):
        self.bind("<Key>", lambda e: self.after_idle(lambda: self.__bind_dealing__(e)))
        self.bind("<Tab>", self.__add_tab__)
        self.bind("<Shift-Tab>", self.__untab__)

    def __bind_dealing__(self, event):
        SHIFT_PRESSED = "ISO_Left_Tab"

        if event.keysym == SHIFT_PRESSED:
            self.__untab__()

    def __add_tab__(self, e):
        index = self.index("insert")
        self.insert(index, " "*self.tab_width)
        self.highlight_selected_line()
        return "break"

    def __untab__(self):
        index = self.index("insert linestart")
        line_start = self.get(index, f"{index} + {self.tab_width}c")

        if line_start.startswith(" " * self.tab_width):
            self.delete(index, f"{index} + {self.tab_width}c")
        elif line_start.startswith("\t"):
            self.delete(index)

        self.highlight_selected_line()
        return "break"

    def create_line_counter(self, master):
        def load_line_counter_theme() -> tuple:
            dark = "_dark" if self.sys_theme == "dark" else ""
            bg_color = self.theme["widgets"]["line_counter"][f"bg{dark}"]
            font_color = self.theme["widgets"]["line_counter"][f"font{dark}"]
            return (bg_color, font_color)
        bg_color, font_color = load_line_counter_theme()

        tilde_char = Application.mainapp.config["nonexistent_char"]
        self._line_counter = TkLineNumbers(
            master, self, justify="right", colors=(font_color, bg_color), tilde=tilde_char, bd=0
        )

        self._line_counter.grid(row=0, column=0, sticky="nsew", pady=(6 * (self._get_widget_scaling()) + 0.5,0))
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


class Lefttext(Generaltext):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        super().enable_auto_highlight_line()

        self.bg_color, self.selected_line_color, self.font_color, self.exp_dir_color, self.exp_file_color, self.exp_curdir_color = super().load_theme(self)
        self.configure(bg_color=self.bg_color, fg_color=self.bg_color, state="disabled")

    def updir(self):
        self.path = os.path.dirname(self.path)
