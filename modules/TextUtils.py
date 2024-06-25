import tkinter

from modules.Application import Application
from modules.CommandManager import CommandManager
from modules.LanguageManager import LanguageManager
from modules.FileManager import FileManager as fm

DELIMITERS = ['{', ':']

# adicionar a possiblidade de selecionar uma área e remover/adicionar tabs


class TextUtils:
    @staticmethod
    def return_manager(e):
        """Runs every Return in all project"""
        if Application.mainapp.left_frame.open_file_or_directory():
            return

    @staticmethod
    def _has_delimiter(t):
        """Checks if the last char in current line is a delimiter"""
        line = t.index("insert").split('.')[0]
        content = (t.get("insert linestart", f"{line}.end"))
        if not content:
            return False
        last_char = content[-1]
        return last_char in DELIMITERS

    @staticmethod
    def add_newline(t):
        """Runs every Return in maintext widget. Adds a newline checking delimiters, tab count, etc"""
        if TextUtils._has_delimiter(t):
            return TextUtils.add_newline_with_tab(t, 1)

        return TextUtils._add_newline(t)

    @staticmethod
    def _add_newline(t):
        """
        Add a newline with tabs. Can break line in half
        event: Return
        """
        i = t.index("insert")
        i_line   = i.split('.')[0]
        i_below = f"{int(i_line) + 1}.0"

        tab_count = TextUtils.get_tab_count(t)
        t.insert(i_below, f"{t.get('insert', 'insert lineend')}\n")
        t.delete('insert', "insert lineend")
        t.mark_set('insert', i_below)

        TextUtils.__add_context_tab__(t, tab_count)
        t.highlight_selected_line()
        t.update_line_counter()
        return "break"

    @staticmethod
    def add_newline_with_tab(t, manual_tabs: int = 0):
        """
        Add a new line with above tab identation. Does not break the current line in half
        event: Control-Return
        """
        i = t.index("insert")
        i_x = i.split('.')[0]
        i_below = f"{int(i_x) + 1}.0"

        tab_count = TextUtils.get_tab_count(t)
        t.insert(i_below, "\n")
        t.mark_set('insert', i_below)

        TextUtils.__add_context_tab__(t, tab_count, manual_tabs)
        t.highlight_selected_line()
        t.update_line_counter()
        return "break"

    @staticmethod
    def get_tab_count(t):
        content = t.get("insert linestart", "insert lineend")
        tab_count = content.split(" "*t.tab_width)
        return tab_count

    @staticmethod
    def __add_context_tab__(t, tab_count, manual_tabs: int = 0):
        """Adds the tab identation for tab_count times in the current line"""
        for i in range(0, manual_tabs):
            TextUtils.add_tab(t)

        for i, tab in enumerate(tab_count):
            if tab != '':
                return "break"
            if i == (len(tab_count) - 1):
                return "break"
            TextUtils.add_tab(t)

    @staticmethod
    def add_tab(t):
        """Simple tab addition. Runs every Tab event"""
        selected_lines = TextUtils.get_selected_lines(t)
        if not selected_lines:
            selected_lines = [t.index("insert")]

        for i in selected_lines:
            i = f"{i}.0" if len(selected_lines) > 1 else i
            t.insert(i, " " * t.tab_width)

        t.highlight_selected_line()
        return "break"

    @staticmethod
    def untab(t):
        """Untab the current line. Runs every Shift-Tab event"""
        selected_lines = TextUtils.get_selected_lines(t)
        if not selected_lines:
            selected_lines = [t.index('insert linestart')]

        for line in selected_lines:
            if len(selected_lines) > 1:
                line = f"{line}.0"
            line_start = t.get(line, f"{line} + {t.tab_width}c")

            if line_start.startswith(" " * t.tab_width):
                t.delete(line, f"{line} + {t.tab_width}c")
            elif line_start.startswith("\t"):
                t.delete(line)

        t.highlight_selected_line()
        return "break"

    @staticmethod
    def comment_lines(t):
        TextUtils._comment_lines_(t)
        t.highlight_selected_line()
        return "break"

    @staticmethod
    def _comment_lines_(t):
        """
        Add a comment symbol in line start
        event: Control-d
        """
        if Application.mode != "insert":
            return False

        fm.move_to_directory("languages")
        comment_symbol = LanguageManager.get_info("comment")
        if not comment_symbol:
            return "break"

        selected_lines = TextUtils.get_selected_lines(t)
        if not selected_lines:
            selected_lines = [t.index("insert").split('.')[0]]

        for line in selected_lines:
            i = f"{line}.0"
            current_line_text = t.get(i, f"{line}.end")

            if current_line_text.startswith(comment_symbol):
                t.delete(i, f"{line}.{len(comment_symbol) + 1}")
            else:
                t.insert(i, f"{comment_symbol} ")
        return True

    @staticmethod
    def get_selected_lines(t):
        try:
            start = t.index("sel.first")
            end   = t.index("sel.last")
            start_line = int(start.split('.')[0])
            end_line = int(end.split('.')[0])
            selected_lines = list(range(start_line, end_line + 1))
            return selected_lines
        except tkinter.TclError:
            return []
