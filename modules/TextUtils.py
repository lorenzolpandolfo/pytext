from modules.Application import Application
from modules.CommandManager import CommandManager

DELIMITERS = ['{', ':']


class TextUtils:
    @staticmethod
    def return_manager(e):
        if Application.mainapp.left_frame.open_file_or_directory():
            return

    @staticmethod
    def _check_if_delimiter(t):
        line = t.index("insert").split('.')[0]
        content = (t.get("insert linestart", f"{line}.end"))
        if not content:
            return False
        last_char = content[-1]
        return last_char in DELIMITERS

    @staticmethod
    def add_newline(t):
        if TextUtils._check_if_delimiter(t):
            return TextUtils.add_newline_with_tab(t, 1)
        t.update_line_counter()
        t.after_idle(t.highlight_selected_line)
        return

    @staticmethod
    def add_newline_with_tab(t, manual_tabs: int = 0):
        i = t.index("insert")
        i_x = i.split('.')[0]
        i_below = f"{int(i_x) + 1}.0"

        content = t.get("insert linestart", "insert lineend")
        tab_count = content.split(" "*t.tab_width)
        t.insert(i_below, "\n")
        t.mark_set('insert', i_below)

        TextUtils.__add_context_tab__(t, tab_count, manual_tabs)
        t.highlight_selected_line()
        t.update_line_counter()
        return "break"

    @staticmethod
    def __add_context_tab__(t, tab_count, manual_tabs: int = 0):
        for i in range(0, manual_tabs):
            TextUtils.add_tab(t)

        for i, tab in enumerate(tab_count):
            if tab != '':
                return "break"
            if i == (len(tab_count) - 1):
                return "break"
            TextUtils.add_tab(t)

    @staticmethod
    def _add_tab_to_newline(t):
        i_x = t.index("insert").split('.')[0]
        if i_x == 0:
            return False

        i_above = f"{int(i_x) - 1}.0"
        line_above_content = t.get(i_above, f"{int(i_above.split('.')[0]) + 1}.0")

        tab_width_count = line_above_content.split(" "*t.tab_width)
        for tab in tab_width_count:
            if tab != '':
                return
            TextUtils.add_tab(t)

    @staticmethod
    def add_tab(t):
        i = t.index("insert")
        t.insert(i, " " * t.tab_width)
        t.highlight_selected_line()
        return "break"

    @staticmethod
    def untab(t):
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
        CommandManager.comment_lines(t)
        t.highlight_selected_line()
        return "break"
