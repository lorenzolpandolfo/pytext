from modules.Application import Application
from modules.CommandManager import CommandManager


class TextUtils:
    @staticmethod
    def return_manager(e):
        if Application.mainapp.left_frame.open_file_or_directory():
            return

    @staticmethod
    def __add_tab__(t):
        i = t.index("insert")
        t.insert(i, " " * t.tab_width)
        t.highlight_selected_line()
        return "break"

    @staticmethod
    def __untab__(t):
        i = t.index("insert linestart")
        line_start = t.get(i, f"{i} + {t.tab_width}c")

        if line_start.startswith(" " * t.tab_width):
            t.delete(i, f"{i} + {t.tab_width}c")
        elif line_start.startswith("\t"):
            t.delete(i)

        t.highlight_selected_line()
        return "break"

    @staticmethod
    def __comment_lines__(t):
        CommandManager.comment_lines(t)
        t.highlight_selected_line()
        return "break"
