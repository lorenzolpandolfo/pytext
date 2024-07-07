import os
import ctypes

import tkinter as tk
from ttkbootstrap import Style

import darkdetect
import platform

from modules.UserConfig import UserConfig
from modules.FontManager import FontManager
from modules.ImageManager import ImageManager
from modules.ThemeManager import ThemeManager
from modules.TextUtils import TextUtils
from modules.Application import Application
from modules.CommandManager import CommandManager
from modules.ScriptRunner import ScriptRunner
from modules.FileLoader import FileLoader

from modules.frames.frames import LeftFrame, BottomFrame, MainFrame


class MainApp(tk.Tk):
    def __init__(self, terminal_path: str, arg_file_title: str):
        super().__init__()
        Application.mainapp = self
        Application.terminal_path = terminal_path

        self.arg_file_title = arg_file_title

        self.__windows_set_dpi_awareness()
        
        self.__load_user_config()
        self.__load_system_theme()
        self.__load_user_font()
        self.__load_user_theme()
        self.__load_ttk_colors()
        self.__create_gui()

        if arg_file_title:
            self.__load_argv_file()
        elif self.user_config["enable_welcome_message"]:
            FileLoader.open_welcome_file()

        self.__enable_binds()

    def __windows_set_dpi_awareness(self):
        scale = self.tk.call('tk', 'scaling')
        if platform.system() == "Windows" and str(scale) != '1.0':
            ctypes.windll.shcore.SetProcessDpiAwareness(1)

    def __load_ttk_colors(self):
        forced_theme = self.user_config["forced_theme"]
        
        if not forced_theme:
            forced_theme = str(darkdetect.theme()).lower()

        dark = "_dark" if forced_theme == "dark" else ""
        selected_tab_color      = self.theme[f"selected_tab{dark}"]
        bg                      = self.theme["frames"]["main"][f"bg{dark}"]
        fg = "#212529"

        if forced_theme == "light":
            theme = "flatly"

        else:
            theme = "darkly"
            fg = "white"

        self.style = Style(theme=theme)

        # desativar/ativar muda a borda (bordercolor = "red")
        self.style.configure("TNotebook", background=bg)
        self.style.configure("TNotebook.Tab", font=FontManager.FILE_FONT, bordercolor="white",
                             background=bg)
        self.style.map("TNotebook.Tab",
                       background=[("selected", selected_tab_color), ("active", selected_tab_color)],
                       foreground=[("selected", fg), ("active", fg)])

        self.style.configure("TFrame", background=bg)
        self.style.configure("TLabel", background=bg, foreground=fg)
        return

    def __load_user_config(self):
        self.user_config = UserConfig.get_user_config()

    def __load_user_font(self):
        user_font = self.user_config["font"]
        FontManager.load_user_font(user_font)

    def __load_system_theme(self):
        forced_theme = self.user_config["forced_theme"]
        self.sys_theme = forced_theme if forced_theme else str(darkdetect.theme()).lower()

    def __load_user_theme(self):
        self.theme = ThemeManager.get_user_theme()

    def __create_gui(self):
        self.__create_window__()
        self.__configure_grids__()
        self.__create_frames__()
        self.__create_widgets__()

    def __create_window__(self):
        self.title("The Pytext Editor Refactored")
        self.geometry(self.user_config["window_size"])
        self.resizable(True, True)
        ImageManager.setup_icon(self)

    def __configure_grids__(self):
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        return

    def __create_frames__(self):
        # A maintext agora está contida no TopBarFrame porque ele tem o Notebook que cria o Maintext
        # topbarframe deve estar ao lado do leftframe
        self.main_frame = MainFrame(self)
        self.main_frame.grid(row=0, column=1, sticky="nsew")

        self.bottom_frame = BottomFrame(self)
        self.bottom_frame.grid(row=2, column=0, sticky="we", columnspan=3)

        self.left_frame = LeftFrame(self)

    def __create_widgets__(self):
        self.left_frame.create_textbox()
        self.bottom_frame.create_widgets()

    def __load_argv_file(self):
        path = os.path.join(Application.terminal_path, self.arg_file_title)
        FileLoader.open_file(path)

    def __enable_binds(self):
        self.bind("<Escape>", lambda _: Application.switch_mode('view'))
        self.bind("<Control-e>", self.left_frame.switch_view)
        self.bind("<Key>", self.key_manager)
        self.bind("<Return>", TextUtils.return_manager)
        self.bind("<Control-F5>", ScriptRunner.run_script)
        self.bind("<Control-w>", lambda e: Application.delete_tab())
        self.bind("<Control-t>", lambda e: self.main_frame.add_tab("untitled", "", Application.terminal_path))

    def key_manager(self, event=None):
        if CommandManager.command_dealing(event):
            self.bottom_frame.clear_command_output()


if __name__ == "__main__":
    import sys
    file_title = sys.argv[1] if len(sys.argv) > 1 else ""
    file_title = file_title[2:] if file_title[:2] == ".\\" else file_title
    is_argv_file = os.path.isfile(os.path.join(os.getcwd(), file_title))
    app = MainApp(terminal_path=os.getcwd(), arg_file_title=file_title)
    app.mainloop()
