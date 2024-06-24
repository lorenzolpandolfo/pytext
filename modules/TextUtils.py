from modules.Application import Application
from modules.CommandManager import CommandManager

DELIMITERS = ['{', ':']

# adicionar a possiblidade de selecionar uma área e remover/adicionar tabs


class TextUtils:
    @staticmethod
    def return_manager(e):
        """Runs every Return in all project"""
        if Application.mainapp.left_frame.open_file_or_directory():
            return

    @staticmethod
    def _check_if_delimiter(t):
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
        if TextUtils._check_if_delimiter(t):
            return TextUtils.add_newline_with_tab(t, 1)

        return TextUtils._add_newline(t)

    @staticmethod
    def _add_newline(t):
        """Add a newline with tabs"""
        i = t.index("insert")
        i_x = i.split('.')[0]
        i_y = i.split('.')[1]
        i_below = f"{int(i_x) + 1}.{i_y}"

        tab_count = TextUtils.get_tab_count(t)
        t.insert(i_below, "\n")
        t.mark_set('insert', i_below)

        TextUtils.__add_context_tab__(t, tab_count)
        t.highlight_selected_line()
        t.update_line_counter()
        return "break"

    @staticmethod
    def add_newline_with_tab(t, manual_tabs: int = 0):
        """Add a new line with above tab identation. Does not break the current line in half"""
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
        i = t.index("insert")
        t.insert(i, " " * t.tab_width)
        t.highlight_selected_line()
        return "break"

    @staticmethod
    def untab(t):
        """Untab the current line. Runs every Shift-Tab event"""
        i = t.index("insert linestart")
        line_start = t.get(i, f"{i} + {t.tab_width}c")

        if line_start.startswith(" " * t.tab_width):
            t.delete(i, f"{i} + {t.tab_width}c")
        elif line_start.startswith("\t"):
            t.delete(i)

        t.highlight_selected_line()
        return "break"

    @staticmethod
    def comment_lines(t):
        """Add a comment symbol in line start. Runs every Control-D event"""
        CommandManager.comment_lines(t)
        t.highlight_selected_line()
        return "break"
