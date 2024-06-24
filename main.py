import os

import tkinter as tk
from tkinter import font as tkfont
import darkdetect

from modules.UserConfig     import UserConfig
from modules.FontManager    import FontManager
from modules.FileManager    import FileManager
from modules.ThemeManager   import ThemeManager
from modules.TextUtils      import TextUtils
from modules.Application    import Application
from modules.CommandManager import CommandManager
from modules.ScriptRunner   import ScriptRunner

from modules.frames.frames import MainFrame, LeftFrame, BottomFrame, LineCounterFrame


class MainApp(tk.Tk):
    def __init__(self, terminal_dir: str, loaded_file_name: str):
        super().__init__()

        self.terminal_dir   = terminal_dir
        self.file_name      = loaded_file_name
        self.mode           = "view"

        Application.mainapp     = self
        CommandManager.mainapp  = self
        Application.set_mode("view")

        self.__load_user_config__()
        self.__load_system_theme__()
        self.__load_user_font__()
        self.__load_user_theme__()
        self.__create_gui__()

        if self.file_name:
            self.__load_argv_file__()
        self.__enable_binds__()

    def __load_user_config__(self):
        self.user_config = UserConfig.get_user_config()

    def __load_user_font__(self):
        user_font = self.user_config["font"]
        loader = FontManager.load_user_font(user_font)

        if isinstance(loader, int):
            print(f"Error: could not load font '{user_font['title']}'. Loading default font instead.")
            self.font     = tkfont.Font(font="Consolas", size=26)
            self.gui_font = tkfont.Font(font="Consolas", size=17)
        else:
            self.font, self.gui_font = loader

    def __load_system_theme__(self):
        forced_theme = self.user_config["forced_theme"]
        # adicionar o estilo do sistema ali no else dark
        self.sys_theme = forced_theme if forced_theme else str(darkdetect.theme()).lower()

    def __load_user_theme__(self):
        self.theme = ThemeManager.get_user_theme()

    def __create_gui__(self):
        self.__create_window__()
        self.__configure_grids__()
        self.__create_frames__()
        self.__create_widgets__()

    def __create_window__(self):
        self.title("The Pytext Editor Refactored")
        self.geometry(self.user_config["window_size"])
        self.resizable(True, True)

    def __configure_grids__(self):
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=0)
        self.grid_columnconfigure(2, weight=2)

    def __create_frames__(self):
        self.bottom_frame = BottomFrame(self)
        self.bottom_frame.grid(row=1, column=0, sticky="we", columnspan=3, rowspan=3)

        self.main_frame = MainFrame(self, self.font)
        self.main_frame.grid(row=0, column=2, sticky="nsew")

        self.left_frame = LeftFrame(self, self.font)

        self.line_counter_frame = LineCounterFrame(self)
        self.line_counter_frame.grid(row=0, column=1, sticky="nsew")

    def __create_widgets__(self):
        self.main_frame.create_textbox()
        self.main_frame.textbox.create_line_counter(self.line_counter_frame)

        self.left_frame.create_textbox()

        self.bottom_frame.create_widgets(output=(self.file_name if self.file_name else "Welcome to Pytext refactored"))

    def __load_argv_file__(self):
        full_path = os.path.join(self.terminal_dir, self.file_name)
        self.main_frame.textbox.open_file(full_path)
        # if FileManager.check_if_repository(full_path):
        #     self.bottom_frame.create_branch_icon(FileManager.get_git_branch(full_path))

    def __enable_binds__(self):
        self.bind("<Escape>",     lambda _: Application.switch_mode('view'))
        self.bind("<Control-e>",  self.left_frame.switch_view)
        self.bind("<Key>",        self.key_manager)
        self.bind("<Return>",     TextUtils.return_manager)
        self.bind("<Control-F5>", ScriptRunner.run_script)

    def key_manager(self, event=None):
        if CommandManager.command_dealing(event):
            self.bottom_frame.clear_command_output()


if __name__ == "__main__":
    import sys
    file_name = sys.argv[1] if len(sys.argv) > 1 else ""
    file_name = file_name[2:] if file_name[:2] == ".\\" else file_name
    is_argv_file = os.path.isfile(os.path.join(os.getcwd(), file_name))
    app = MainApp(terminal_dir=os.getcwd(), loaded_file_name=file_name)
    app.mainloop()
