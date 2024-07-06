import tkinter as tk
import re

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

    @classmethod
    def apply_syntax_highlight(cls, t):
        dc = {
            "operators": ["+", "-", "*", "/", "//", "%", "**", "==", "!=", ">", "<", ">=", "<=", "&", "|", "^", "~",
                          "<<", ">>", "and", "or", "not", "is", "in"],
            "statements": ["if", "elif", "else", "for", "while", "break", "continue", "return", "pass", "with", "as",
                           "try", "except", "finally", "raise", "import", "from", "def", "class", "lambda", "global",
                           "nonlocal", "assert", "yield", "del"],
            "data_types": ["int", "float", "complex", "list", "tuple", "range", "str", "set", "frozenset", "dict",
                           "bool", "bytes", "bytearray", "memoryview"],
            "built_in_functions": ["abs", "all", "any", "ascii", "bin", "bool", "bytearray", "bytes", "callable", "chr",
                                   "classmethod", "compile", "complex", "delattr", "dict", "dir", "divmod", "enumerate",
                                   "eval", "exec", "filter", "float", "format", "frozenset", "getattr", "globals",
                                   "hasattr", "hash", "help", "hex", "id", "input", "int", "isinstance", "issubclass",
                                   "iter", "len", "list", "locals", "map", "max", "memoryview", "min", "next", "object",
                                   "oct", "open", "ord", "pow", "print", "property", "range", "repr", "reversed",
                                   "round", "set", "setattr", "slice", "sorted", "staticmethod", "str", "sum", "super",
                                   "tuple", "type", "vars", "zip"],
            "exceptions": ["BaseException", "Exception", "ArithmeticError", "BufferError", "LookupError",
                           "AssertionError", "AttributeError", "EOFError", "FloatingPointError", "GeneratorExit",
                           "ImportError", "ModuleNotFoundError", "IndexError", "KeyError", "KeyboardInterrupt",
                           "MemoryError", "NameError", "NotImplementedError", "OSError", "OverflowError",
                           "RecursionError", "ReferenceError", "RuntimeError", "StopIteration", "SyntaxError",
                           "IndentationError", "TabError", "SystemError", "SystemExit", "TypeError",
                           "UnboundLocalError", "UnicodeError", "UnicodeEncodeError", "UnicodeDecodeError",
                           "UnicodeTranslateError", "ValueError", "ZeroDivisionError"],
            "keywords": ["False", "None", "True", "and", "as", "assert", "async", "await", "break", "class", "continue",
                         "def", "del", "elif", "else", "except", "finally", "for", "from", "global", "if", "import",
                         "in", "is", "lambda", "nonlocal", "not", "or", "pass", "raise", "return", "try", "while",
                         "with", "yield"]
        }

        ndc = ["import ", " from ", "def ", "class ", "return ", "if ", " in "]
        visible_lines = cls.get_visible_lines(t)
        visible_content = t.get(visible_lines[0], visible_lines[1]).split("\n")

        print("-"*30)
        for n, line in enumerate(visible_content):
            cur_line = n + float(visible_lines[0])
            pattern = r'\b(' + '|'.join(ndc) + r')\b'

            for m in re.finditer(pattern, line):
                keyword = m.group(0)
                first_index = m.start()
                print(f"[Linha {cur_line}] keyword encontrada: {keyword} em {first_index}.{first_index+len(keyword)}")

    @staticmethod
    def add_tag_to_word(t, first_index, last_index):
        # t.tag_remove("keyword", "1.0", "end")
        t.tag_add("keyword", first_index, last_index)
        t.tag_config("keyword", background="red")

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
