from typing import Any
from uuid import uuid4
from tkinter import font, ttk
from ttkbootstrap import Scrollbar, Label, Notebook, Style
import os
from modules.widgets.text import Lefttext, Maintext
from modules.Application import Application
from modules.FileLoader import FileLoader
from modules.FontManager import FontManager

DEFAULT_SIZE_OF_EXPLORER_TEXT_WIDGET = 20


class LeftFrame(ttk.Frame):
    """ Contains the file explorer. """
    def __init__(self, master):
        super().__init__(master)
        self.textbox = None

        self.__grid_setup()
        self.__scrollbar_setup()

    def __scrollbar_setup(self):
        self.scrollbar_x = Scrollbar(self, orient="horizontal", command=self.__scroll_x)
        self.scrollbar_x.grid(row=1, column=0, sticky="we")

    def __scroll_x(self, *args):
        self.textbox.xview(*args)

    def __grid_setup(self):
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        return

    def create_textbox(self, row: int = 0, column: int = 0):
        self.textbox = Lefttext(
            self, font=FontManager.GUI_FONT, width=DEFAULT_SIZE_OF_EXPLORER_TEXT_WIDGET, wrap='none'
        )
        self.textbox.config(xscrollcommand=self.scrollbar_x.set)

    def show_textbox(self):
        self.after_idle(lambda: self.grid(row=0, column=0, sticky="nsew"))
        self.after_idle(lambda: self.textbox.grid(row=0, column=0, sticky="nsew"))
        file_directory_path = Application.current_file_directory
        self.textbox.open_directory(file_directory_path)
        self.textbox.focus_set()

    def switch_view(self, e=None):
        if self.winfo_ismapped():
            if "leftframe" in str(self.focus_get()):
                self.grid_forget()
                if Application.has_any_tab_open():
                    Application.selected_tab_frame.textbox.focus_set()
            else:
                self.textbox.focus_set()
        else:
            self.show_textbox()

    def open_file_or_directory(self):
        if "leftframe" not in str(self.focus_get()):
            return False

        side_bar_selected_file_name = self.textbox.get_current_line_content().strip()
        if side_bar_selected_file_name[0] == "▼":
            self.textbox.updir()
            return

        elif side_bar_selected_file_name[0] == "/":
            side_bar_selected_file_name = side_bar_selected_file_name[1:]

        content = os.path.join(self.textbox.path, side_bar_selected_file_name)

        if os.path.isdir(content):
            self.textbox.open_directory(content)
            return
        else:
            # contar quantos diretorios tem antes e ir salvando a posicao do cursor pra retomar
            FileLoader.open_file(content)


class BottomFrame(ttk.Frame):
    """Contains the outputs labels."""

    def __init__(self, master):
        super().__init__(master)
        self.output = None
        self.command = None
        self.mode = None

    def create_widgets(self):
        self.mode = Label(
            self, justify="center",
            font=FontManager.GUI_FONT
        )

        self.command = Label(
            self, justify="left",
            font=FontManager.GUI_FONT
        )

        self.output = Label(
            self, justify="left",
            font=FontManager.GUI_FONT
        )

        self.grid_columnconfigure(1, weight=1)
        self.output.grid(row=2, column=0)
        self.mode.grid(row=1, column=0, columnspan=2)
        self.command.grid(row=2, column=1, sticky="e")

    def clear_command_output(self):
        self.command.configure(text='')


class TextFrame(ttk.Frame):
    """It is the main frame that contains the Maintext instance."""

    def __init__(self, master, obj_font: font):
        super().__init__(master)
        self.master = master
        self.textbox = None
        self.font = obj_font

        self.__grid_setup()

    def create_textbox(self, row: int = 1, column: int = 2):
        self.textbox = Maintext(self, font=self.font)
        self.textbox.grid(row=1, column=1, sticky="nsew")
        self.master.update()
        self.textbox.focus_set()

    def __grid_setup(self):
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(1, weight=1)
        return


class MainFrame(ttk.Frame):
    notebook = None

    def __init__(self, master, *a, **kw):
        super().__init__(master, *a, **kw)
        # remover o master. So é utilizado pra font
        self.master = master
        self.notebook = Notebook(self)
        self.current_frame = None
        self.__setup()

        self.notebook.bind("<<NotebookTabChanged>>", lambda e: self.__on_tab_change(e))
        # self.notebook.bind("<<TabClosed>>", lambda e: print("tab closed"))
        # self.notebook.bind("<<TabOpened>>", lambda e: print("tab opened!"))

    def __on_tab_change(self, e=None):
        if not Application.has_any_tab_open():
            Application.switch_mode("view", False)
            return
        Application.mainapp.update()
        Application.mainapp.update_idletasks()
        Application.selected_tab_frame = self.notebook.nametowidget(self.notebook.select())

        for tab_id, data in Application.all_open_files.items():
            if str(data["frame"]) == str(self.notebook.select()):
                Application.set_current_file(data["file_path"])
                self.notebook.select(data["frame"])

        Application.switch_mode("view")
        Application.selected_tab_frame.textbox.focus_set()
        self.notebook.event_generate("<<TabOpened>>")

    def add_tab(self, tab_title: str, content: str, file_path: str):
        """
        Creates a new MainFrame to the Notebook bar.
        In the MainFrame, creates the textbox and the line counter.
        Inserts text into the textbox.
        """
        file_title = os.path.basename(file_path)

        if file_title != tab_title:
            file_path = os.path.join(file_path, tab_title)

        existent_tab_id = MainFrame.tab_exist(file_path)
        if existent_tab_id:
            widget_frame = existent_tab_id[1]["frame"]
            index_widget_frame = self.notebook.index(widget_frame)
            self.notebook.select(index_widget_frame)
            return

        self.current_frame = TextFrame(self.notebook, FontManager.FILE_FONT)
        self.notebook.add(self.current_frame, text=tab_title, sticky="nsew")
        Application.mainapp.update()

        self.current_frame.create_textbox()
        self.current_frame.textbox.create_line_counter(self.current_frame)

        tab_id = str(uuid4())
        Application.all_open_files[tab_id] = {
            "title": tab_title,
            "frame": self.current_frame,
            "file_path": file_path
        }
        self.current_frame.textbox.write_file_content(content)
        self.notebook.select(self.current_frame)
        Application.selected_tab_frame = self.current_frame

    def __setup(self):
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.notebook.grid(row=0, column=0, sticky="nsew")

    @staticmethod
    def tab_exist(file_path: str) -> tuple[Any, Any] | bool:
        for frame_id, data in Application.all_open_files.items():
            if str(data["file_path"]) == str(file_path):
                return frame_id, data
        return False
