import tkinter as tk
import re

import pygments
from pygments import lexer, lexers
from pygments.lexers import PythonLexer

from modules.Application import Application
from modules.LanguageManager import LanguageManager
from modules.FileManager import FileManager as fm

DELIMITERS = [':', '{', '}', '(', ')']


class TextUtils:
    @staticmethod
    def return_manager(e=None):
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
        """
        Add a newline with tabs. Can break line in half
        event: Return
        """
        i = t.index("insert")
        i_line   = i.split('.')[0]
        i_below = f"{int(i_line) + 1}.0"

        i_last_line = t.index('end').split('.')[0]

        tab_count = TextUtils.get_tab_count(t)

        # if user is using Return in the last line
        if int(i_last_line) == int(i_line) + 1:
            content = t.get(i, 'insert lineend')
            t.delete('insert', "insert lineend")
            t.insert('insert lineend', '\n')
            t.mark_set('insert', i_below)
            t.insert(i_below, content)
            t.highlight_selected_line()
            t.update_line_counter()
            return 'break'

        t.insert(i_below, f"{t.get('insert', 'insert lineend')}\n")
        t.delete('insert', "insert lineend")
        t.mark_set('insert', i_below)

        if not TextUtils.is_cursor_visible(t):
            t.yview_scroll(1, "units")

        TextUtils.__add_context_tab(t, tab_count)
        t.highlight_selected_line()
        t.update_line_counter()
        return "break"

    @staticmethod
    def is_cursor_visible(t):
        cursor_index = t.index('insert')
        visible_range = t.yview()
        cursor_line = int(cursor_index.split('.')[0])

        first_visible_line = int(float(visible_range[0]) * int(t.index('end').split('.')[0]))
        last_visible_line = int(float(visible_range[1]) * int(t.index('end').split('.')[0]))

        return first_visible_line <= cursor_line <= last_visible_line

    @staticmethod
    def get_visible_lines(t) -> tuple[str, str]:
        visible_range = t.yview()
        first_visible_line = int(float(visible_range[0]) * int(t.index('end').split('.')[0])) + 1
        last_visible_line = int(float(visible_range[1]) * int(t.index('end').split('.')[0])) + 1
        return f"{first_visible_line}.0", f"{last_visible_line}.0"

    @staticmethod
    def highlight_line(t, line: int = None):
        TextUtils.clear_all_tags(t)
        if line is None:
            line = int(t.index("insert").split(".")[0])
        content = t.get(f"{line}.0", f"{line}.end")
        start = f"{line}.0"

        for tag in t.tag_names(index=None):
            if tag != "sel" and tag != "current_line_color":
                t.tag_remove(tag, f"{line}.0", f"{line}.end")

        for token, content in pygments.lex(content, PythonLexer()):
            end = f"{start.split('.')[0]}.{int(start.split('.')[1]) + len(content)}"
            t.tag_add(str(token), start, end)
            start = end

    @classmethod
    def highlight_visible_lines(cls, t):
        visible_lines = cls.get_visible_lines(t)
        first_line = int(visible_lines[0].split('.')[0])
        last_line = int(visible_lines[1].split('.')[0])
        # print(first_line, last_line, "\n", t.last_start_visible_line, t.last_final_visible_line)

        if first_line == t.last_start_visible_line and last_line == t.last_final_visible_line:
            # print("ignorado")
            return

        # print("qtd de tags: ", len(t.tag_names()))
#         for tag in t.tag_names():
#             if tag != "sel" and tag != "current_line_color":
#                 t.tag_remove(tag, "1.0", "end")
        cls.clear_all_tags(t)

        for line in range(first_line, last_line):
            cls.highlight_line(t, line)
        
        t.last_start_visible_line = first_line
        t.last_final_visible_line = last_line


    @classmethod
    def smart_syntax_highlight(cls, t):
        # print("-"*30)
        visible_lines = cls.get_visible_lines(t)
        first_line = int(visible_lines[0].split('.')[0])
        last_line = int(visible_lines[1].split('.')[0])

        # if t.last_start_visible_line and t.last_final_visible_line:
            # for line in range(t.last_final_visible_line, last_line):
                # print(line)
                # cls.highlight_line(t, line)

        t.last_start_visible_line = first_line
        t.last_final_visible_line = last_line

    @classmethod
    def clear_all_tags(cls, t):
        visible_lines = cls.get_visible_lines(t)

        for tag in t.tag_names():
            # print(f"removendo de 1.0 até {visible_lines[0]} e {visible_lines[1]} até end")
            t.tag_remove(tag, "1.0", visible_lines[0])
            t.tag_remove(tag, visible_lines[1], "end")

    @staticmethod
    def add_newline_with_tab(t):
        """
        Add a new line with above tab identation. Does not break the current line in half
        event: Control-Return
        """
        manual_tabs = 0

        if TextUtils._has_delimiter(t):
            manual_tabs = 1

        i = t.index("insert")
        i_x = i.split('.')[0]
        i_below = f"{int(i_x) + 1}.0"

        tab_count = TextUtils.get_tab_count(t)
        t.insert(i_below, "\n")
        t.mark_set('insert', i_below)

        TextUtils.__add_context_tab(t, tab_count, manual_tabs)
        t.highlight_selected_line()
        t.update_line_counter()
        return "break"

    @staticmethod
    def get_tab_count(t):
        content = t.get("insert linestart", "insert lineend")
        tab_count = content.split(" "*t.tab_width)
        return tab_count

    @staticmethod
    def __add_context_tab(t, tab_count, manual_tabs: int = 0):
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
        except tk.TclError:
            return []

    @staticmethod
    def swipe_lines(t: tk.Text, l1: str | int, l2: str | int):
        """Move content from line1 to line2. l is the line number, with no columns."""
        selected_lines = TextUtils.get_selected_lines(t)
        if selected_lines:
            direction = "up" if (int(l1) < int(l2)) else "down"
            return TextUtils.swipe_block(t, selected_lines, direction)

        if int(l1) > int(t.index("end-1c").split('.')[0]):
            return False

        c1 = t.get(f"{l1}.0", f"{l1}.end")
        c2 = t.get(f"{l2}.0", f"{l2}.end")

        t.delete(f"{l1}.0", f"{l1}.end")
        t.insert(f"{l1}.0", c2)
        t.delete(f"{l2}.0", f"{l2}.end")
        t.insert(f"{l2}.0", c1)
        t.edit_separator()

    @staticmethod
    def swipe_block(t: tk.Text, b: tuple | list, direction: str):
        if isinstance(b, list):
            b = (b[0], b[-1])

        c = t.get(f"{b[0]}.0", f"{b[1]}.end")

        if direction == "up":
            if b[0] == 1:
                return False

            target = f"{b[0] - 1}.0"
            target_c = t.get(target, f"{b[0] - 1}.end")
            t.delete(f"{b[0]}.0", f"{b[1]}.end")
            t.delete(target, f"{b[0] - 1}.end")
            t.insert(target, c)
            t.insert(f"{b[1]}.0", target_c)
            t.tag_remove("sel", "1.0", "end")
            t.tag_add("sel", f"{b[0] - 1}.0", f"{b[1] - 1}.end")
            t.edit_separator()

        elif direction == "down":
            if b[1] == int(t.index("end-1c").split('.')[0]):
                return False

            target = f"{b[0] + 1}.0"
            target_c = t.get(f"{b[1] + 1}.0", f"{b[1] + 1}.end")
            t.delete(f"{b[0]}.0", f"{b[1]}.end")
            t.delete(target, f"{b[0] + 1}.end")
            t.insert(target, c)
            t.insert(f"{b[0]}.0", target_c)
            t.tag_remove("sel", "1.0", "end")
            t.tag_add("sel", f"{b[0] + 1}.0", f"{b[1] + 1}.end")
            t.edit_separator()
