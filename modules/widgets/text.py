from tkinter import Text
import os

from modules.FileManager     import FileManager
from modules.tklinenums      import TkLineNumbers
from modules.Application     import Application
from modules.TextUtils       import TextUtils
from modules.LanguageManager import LanguageManager


class Generaltext(Text):
    """ Includes methods that Maintext and Lefttext use. """
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs, insertofftime=0)
        self.font_color             : str = ''
        self.bg_color               : str = ''
        self.exp_curdir_color       : str = ''
        self.exp_file_color         : str = ''
        self.exp_dir_color          : str = ''
        self.selected_line_color    : str = ''
        self.path                   : str = ''

        self.sys_theme = master.sys_theme
        self.theme = master.theme
        self.tab_width = Application.mainapp.user_config["tab_width"]
        self.setup_text_widget()

    def setup_text_widget(self):
        dark = "_dark" if self.sys_theme == "dark" else ""
        cursor_color = self.theme[f"cursor_color{dark}"]
        self.configure(
            bd=0, highlightthickness=0, blockcursor=True,
            insertbackground=cursor_color, insertunfocussed="hollow")

    def enable_auto_highlight_line(self):
        self.bind("<Key>",      lambda _: self.after_idle(self.highlight_selected_line))
        self.bind("<Button-1>", lambda _: self.after_idle(self.highlight_selected_line))

    def highlight_selected_line(self):
        line_start = int(self.index("insert").split(".")[0])
        self.tag_remove("current_line_color", "1.0", "end")
        self.tag_add("current_line_color", f"{line_start}.0", f"{line_start + 1}.0")
        self.tag_config("current_line_color", background=self.selected_line_color)

    def load_theme(self, widget):
        dark = "_dark" if self.sys_theme == "dark" else ""
        self.bg_color            = self.theme["widgets"][widget][f"bg{dark}"]
        self.selected_line_color = self.theme["widgets"][widget][f"selected_line{dark}"]
        self.font_color          = self.theme["widgets"][widget][f"font{dark}"]
        self.exp_dir_color       = self.theme["explorer"][f"dir{dark}"]
        self.exp_file_color      = self.theme["explorer"][f"file{dark}"]
        self.exp_curdir_color    = self.theme["explorer"][f"curdir{dark}"]

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

        _, file_ext = os.path.splitext(full_path)
        LanguageManager.load_language(file_ext)
        Application.set_current_file(full_path)
        return content

    def open_directory(self, dir_path: str, auto_write: bool = True):
        content = FileManager.open_directory(dir_path)
        if content:
            self.path = dir_path

            if auto_write:
                self.write_directory_content(
                    content,
                    colors=(self.exp_dir_color, self.exp_file_color, self.exp_curdir_color)
                )

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
        self._enable_binds_()

    def __load_theme__(self):
        super().load_theme("main_textbox")
        self.configure(bg=self.bg_color, foreground=self.font_color, state="disabled")

    def _enable_binds_(self):
        self.bind("<Key>", lambda e: self.after_idle(self.__key_dealing__))
        self.bind("<Tab>", lambda e: TextUtils.add_tab(self))
        self.bind("<ISO_Left_Tab>", lambda e: TextUtils.untab(self))
        self.bind("<Control-d>", lambda e: TextUtils.comment_lines(self))
        self.bind("<Control-Return>", lambda e: TextUtils.add_newline_with_tab(self))
        self.bind("<Return>", lambda e: TextUtils.add_newline(self))

    def __key_dealing__(self):
        self.highlight_selected_line()
        self.update_line_counter()

    def create_line_counter(self, master):
        dark = "_dark" if self.sys_theme == "dark" else ""
        lc_bg_color = self.theme["widgets"]["line_counter"][f"bg{dark}"]
        lc_font_color = self.theme["widgets"]["line_counter"][f"font{dark}"]
        tilde_char = Application.mainapp.user_config["nonexistent_char"]
        self._line_counter = TkLineNumbers(
            master, self, justify="right", colors=(lc_font_color, lc_bg_color), tilde=tilde_char, bd=0
        )
        self._line_counter.grid(row=0, column=0, sticky="nsew", pady=(0, 0))
        self.__enable_auto_redraw__()

    def __enable_auto_redraw__(self):
        self.configure(yscrollcommand=self.__y_scroll_command__)

    def __y_scroll_command__(self, *args):
        return self.update_line_counter()

    def update_line_counter(self):
        Application.mainapp.update()
        Application.mainapp.update_idletasks()
        Application.mainapp.after_idle(self._line_counter.redraw)


class Lefttext(Generaltext):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        super().enable_auto_highlight_line()
        super().load_theme("left_textbox")
        self.configure(bg=self.bg_color, state="disabled", border=False)

    def updir(self):
        self.path = os.path.dirname(self.path)
        self.open_directory(self.path)
