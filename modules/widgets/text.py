import tkinter
from tkinter import Text, Menu, font
import os
import platform

from modules.FileManager     import FileManager
from modules.tklinenums      import TkLineNumbers
from modules.Application     import Application
from modules.TextUtils       import TextUtils
from modules.FileLoader import FileLoader

from modules.Renamer import Renamer


class Generaltext(Text):
    """ Includes methods that Maintext and Lefttext use. """
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs, insertofftime=0)
        self.current_file_content = None
        self.can_open_files         = False
        self.font_color             = ''
        self.bg_color               = ''
        self.exp_curdir_color       = ''
        self.exp_file_color         = ''
        self.exp_dir_color          = ''
        self.selected_line_color    = ''
        self.path                   = ''

        self.last_start_visible_line = None
        self.last_final_visible_line = None

        self.sys_theme = Application.mainapp.sys_theme
        self.theme = Application.mainapp.theme
        self.tab_width = Application.mainapp.user_config["tab_width"]
        self.setup_text_widget()

    def setup_text_widget(self):
        dark = "_dark" if self.sys_theme == "dark" else ""
        cursor_color = self.theme[f"cursor_color{dark}"]
        self.configure(
            bd=0, highlightthickness=0, blockcursor=True,
            insertbackground=cursor_color, insertunfocussed="hollow")

    def enable_binds(self):
        self.bind("<Key>", lambda _: self.after_idle(self.highlight_selected_line))
        self.bind("<Button-1>", self.click_deal)
        self.bind("<Double-Button-1>", self.double_click_deal)

    def highlight_selected_line(self):
        line_start = int(self.index("insert").split(".")[0])
        self.tag_remove("current_line_color", "1.0", "end")
        self.tag_add("current_line_color", f"{line_start}.0", f"{line_start + 1}.0")
        self.tag_config("current_line_color", background=self.selected_line_color)

    def click_deal(self, e):
        click_i = self.index(f"@{e.x},{e.y}")
        self.after(1, lambda: self.mark_set('insert', click_i))
        self.after(1, self.highlight_selected_line)
        return True

    def double_click_deal(self, e=None):
        if self.can_open_files:
            Application.mainapp.left_frame.open_file_or_directory()
            return 'break'

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

    def open_directory(self, dir_path: str, auto_write: bool = True):
        content = FileManager.open_directory(dir_path)
        if content:
            self.path = dir_path

            if auto_write:
                self.write_directory_content(
                    content,
                    colors=(self.exp_dir_color, self.exp_file_color, self.exp_curdir_color)
                )
            self.after(1, lambda: self.tag_remove('sel', '1.0', 'end'))
            self.current_file_content = content[0]

    def focus_set(self):
        super().focus_set()
        self.after_idle(self.highlight_selected_line)

    def get_current_line_content(self):
        line_start = int(self.index("insert").split(".")[0])
        return self.get(f"{line_start}.0", f"{line_start + 1}.0")


class Maintext(Generaltext):
    """Represents the main textbox of Pytext."""
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, undo=True, autoseparators=False, *args, **kwargs)
        self._line_counter = None
        self.sys_theme = Application.mainapp.sys_theme
        self.theme = Application.mainapp.theme
        self.__load_theme()
        super().enable_binds()
        self._enable_binds()
        self.load_syntax_highlight_theme()

    def __load_theme(self):
        super().load_theme("main_textbox")
        self.configure(bg=self.bg_color, foreground=self.font_color, state="disabled")

    def _enable_binds(self):
        shift_tab = "<Shift-Tab>" if platform.system() == "Windows" else "<ISO_Left_Tab>"

        self.bind("<Key>", lambda e: self.after_idle(self.__key_dealing))
        self.bind("<Tab>", lambda e: TextUtils.add_tab(self))
        self.bind(f"{shift_tab}", lambda e: TextUtils.untab(self))
        self.bind("<Shift-Tab>", lambda e: TextUtils.untab(self))
        self.bind("<Control-d>", lambda e: TextUtils.comment_lines(self))
        self.bind("<Control-Return>", lambda e: TextUtils.add_newline_with_tab(self))
        self.bind("<Return>", lambda e: TextUtils.add_newline(self))
        self.bind("<Control-c>", self.copy)
        self.bind("<Control-x>", self.cut)
        self.bind("<Control-v>", self.paste)
        self.bind("<Alt-Shift-Up>", lambda e: self.clone_line(e, "up"))
        self.bind("<Alt-Shift-Down>", lambda e: self.clone_line(e, "down"))
        self.bind("<Alt-Up>", lambda e: self.move_line(e, "up"))
        self.bind("<Alt-Down>", lambda e: self.move_line(e, "down"))
        self.bind("<Control-z>", lambda e: self.undo())
        self.bind("<Control-y>", lambda e: self.redo())
        self.bind("<Control-Tab>", Application.change_to_next_tab)
        self.bind("<Control-comma>", lambda _: FileLoader.open_config_file())
        self.bind("<Control-equal>", lambda _: self.change_font_size(1))
        self.bind("<Control-minus>", lambda _: self.change_font_size(-1))

    def undo(self):
        try:
            self.edit_undo()
            self.after_idle(self.update_line_counter)
            self.highlight_selected_line()
        except tkinter.TclError:
            pass
        return 'break'

    def redo(self):
        try:
            self.edit_redo()
            self.after_idle(self.update_line_counter)
            self.highlight_selected_line()
        except tkinter.TclError:
            pass
        return 'break'

    def move_line(self, e, direction: str):
        i = self.index("insert")
        line = i.split('.')[0]
        content = ''

        if direction == "up":
            if line == '1':
                return 'break'
            TextUtils.swipe_lines(self, int(line) - 1, line)
            self.mark_set("insert", f"{int(line) - 1}.0")

        elif direction == "down":
            TextUtils.swipe_lines(self, int(line) + 1, line)
            self.mark_set("insert", f"{int(line) + 1}.0")

        self.after_idle(self.update_line_counter)
        self.after_idle(self.highlight_selected_line)
        return 'break'

    def clone_line(self, e, direction: str):
        i = self.index("insert")
        line = i.split('.')[0]
        content = self.get("insert linestart", "insert lineend")
        if direction == "up":
            if line == '1':
                return 'break'
            self.insert(f"{line}.0", f"{content}\n")
        elif direction == "down":
            self.insert(f"{int(line) + 1}.0", f"{content}\n")
        self.after_idle(self.update_line_counter)
        self.after_idle(self.highlight_selected_line)
        return 'break'

    def copy(self, e=None):
        self.edit_separator()
        self.clipboard_clear()
        selected_area = len(TextUtils.get_selected_lines(self)) > 0
        if selected_area:
            content = self.get('sel.first', 'sel.last')
            self.clipboard_append(content)
            return 'break'

        content = self.get('insert linestart', 'insert lineend')
        self.clipboard_append(content)
        return 'break'

    def cut(self, e=None):
        self.copy()
        self.delete("insert linestart", "insert lineend+1c")

    def paste(self, e=None):
        self.edit_separator()
        content = f"{self.clipboard_get()}\n"
        self.insert('insert', content)
        return 'break'

    def __key_dealing(self):
        TextUtils.highlight_line(self)
        # TextUtils.highlight_visible_lines(self)
        self.highlight_selected_line()
        self.update_line_counter()

    def load_syntax_highlight_theme(self):
        self.tag_config("Token.Keyword", foreground="#CF8E6D")  # Laranja suave
        self.tag_config("Token.Keyword.Namespace", foreground="#CF8E6D")
        self.tag_config("Token.Literal.String.Single", foreground="#6AAB73")  # Verde suave
        self.tag_config("Token.Literal.String.Double", foreground="#6AAB73")
        self.tag_config("Token.Operator", foreground="#a9b7c6")  # Azul acinzentado
        self.tag_config("Token.Name.Builtin", foreground="#ffc66d")  # Amarelo suave
        self.tag_config("Token.Comment", foreground="#7A7E85")  # Cinza suave
        self.tag_config("Token.Comment.Single", foreground="#7A7E85")  # Cinza suave
        self.tag_config("Token.Name.Function", foreground="#56A8F5")  # Amarelo suave
        self.tag_config("Token.Name.Class", foreground="#C77DBB")  # Amarelo suave
        self.tag_config("Token.Name.Decorator", foreground="#B3AE60")  # Amarelo
        self.tag_config("Token.Literal.Number", foreground="#2AACB8")  # Azul suave
        self.tag_config("Token.Name.Variable", foreground="#a9b7c6")  # Azul acinzentado
        self.tag_config("Token.Text", foreground="#a9b7c6")  # Azul acinzentado
        self.tag_config("Token.Name", foreground="#a9b7c6")  # Azul acinzentado

    def create_line_counter(self, frame):
        dark = "_dark" if self.sys_theme == "dark" else ""
        lc_bg_color = self.theme["widgets"]["line_counter"][f"bg{dark}"]
        lc_font_color = self.theme["widgets"]["line_counter"][f"font{dark}"]
        tilde_char = Application.mainapp.user_config["nonexistent_char"]
        self._line_counter = TkLineNumbers(
            frame, self, justify="right", colors=(lc_font_color, lc_bg_color), tilde=tilde_char, bd=0
        )
        self._line_counter.grid(row=1, column=0, sticky="ns", pady=(0, 0))
        self.__enable_auto_redraw()

    def __enable_auto_redraw(self):
        self.configure(yscrollcommand=self.__y_scroll_command)

    def __y_scroll_command(self, *args):
        self.update_line_counter()

        if Application.selected_tab_frame:
            TextUtils.highlight_visible_lines(Application.selected_tab_frame.textbox)
            # TextUtils.smart_syntax_highlight(Application.selected_tab_frame.textbox)
            pass
        return

    def update_line_counter(self):
        Application.mainapp.update()
        Application.mainapp.update_idletasks()
        Application.mainapp.after_idle(self._line_counter.redraw)

    def change_font_size(self, value: int):
        cur_font = self.cget("font")
        f = font.Font(font=cur_font)
        family = f.actual()["family"]
        size = f.actual()["size"]
        self.configure(font=font.Font(family=family, size=(size + value)))


class Lefttext(Generaltext):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        super().enable_binds()
        self.can_open_files = True
        super().load_theme("left_textbox")
        self.configure(bg=self.bg_color, state="disabled", border=False)

        self.bind("<B1-Motion>", 'break')
        self.bind("<F2>", lambda _: Renamer.create_rename_window())
        self.bind("<Shift-colon>", lambda _: Application.selected_tab_frame.textbox.focus_set())
        self.bind("<Key>", lambda e: self.add_to_searchbar(e))
        self.bind("<BackSpace>", lambda _: self.remove_from_searchbar())
        self.bind("<Control-BackSpace>", lambda _: self.clear_spacebar())

    def add_to_searchbar(self, e):
        if not e.char.isalpha():
            self.after_idle(self.highlight_selected_line)
            return
        content = self.master.searchbar.cget("text")
        if content == "Search...":
            self.master.searchbar.configure(text='')
            content = ''

        new_content = content + e.char
        self.master.searchbar.configure(text=new_content)
        self.after_idle(lambda: self.filter_by_prefix(new_content))

    def filter_by_prefix(self, prefix: str):
        if prefix == "":
            path = Application.current_file_directory if Application.current_file_directory else Application.terminal_path
            self.open_directory(path)
            return
        self.configure(state="normal")
        all_lines = self.current_file_content.split('\n')
        self.delete("1.0", "end")

        index = 1
        for line in all_lines:
            line = line.strip().replace('/', '')
            line_range = line[0:len(prefix)]

            if line_range == prefix:
                index += 1
                self.insert(f"{index}.0", f"{line}\n")

        self.delete("end-1c", "end")
        self.configure(state="disabled")
        self.after_idle(self.highlight_selected_line)

    def remove_from_searchbar(self, e=None):
        content = self.master.searchbar.cget("text")

        if len(content) == 1:
            self.master.searchbar.configure(text="Search...")
            path = Application.current_file_directory if Application.current_file_directory else Application.terminal_path
            self.open_directory(path)
            return
        if content == "Search...":
            return
        content_minus_one = content[0:len(content)-1]
        self.master.searchbar.configure(text=content_minus_one)
        self.after_idle(lambda: self.filter_by_prefix(content_minus_one))

    def clear_spacebar(self, e=None):
        self.master.searchbar.configure(text='')

    def updir(self):
        self.path = os.path.dirname(self.path)
        self.open_directory(self.path)
