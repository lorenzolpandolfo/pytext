import os.path
from dataclasses import dataclass
from typing import Any

import tkinter as tk
from ttkbootstrap import Notebook


@dataclass
class Application:
    mainapp: None

    all_open_files = {}
    selected_tab_frame: Any

    current_file_path       = ""
    current_file_directory  = ""
    terminal_path           = ""
    mode                    = "view"

    @classmethod
    def set_mode(cls, arg: str):
        cls.mode = arg
    
    @classmethod
    def get_mode(cls):
        return cls.mode
    
    @classmethod
    def switch_mode(cls, forced_set: str = '', textbox_state_deal: bool = True):
        cls.mode = forced_set if forced_set else "view" if cls.mode == "insert" else "insert"
        cls.mainapp.bottom_frame.mode.configure(text=cls.mode)
        state = "disabled" if cls.mode == "view" else "normal"
        cls.mainapp.bottom_frame.command.configure(text="")
        if textbox_state_deal:
            cls.selected_tab_frame.textbox.configure(state=state)

    @classmethod
    def set_current_file(cls, path):
        visual_path = path
        cls.mainapp.file_title = path
        cls.current_file_path = path
        cls.current_file_directory = os.path.dirname(path)

        if not os.path.isfile(path):
            visual_path = f"{path} (new)"
        cls.mainapp.bottom_frame.output.configure(text=visual_path)

    @classmethod
    def delete_tab(cls, file_path: str = ""):
        if not file_path:
            file_path = cls.current_file_path
        for frame_id, data in cls.all_open_files.items():
            if str(data["file_path"]) == str(file_path):
                cls.mainapp.top_frame.notebook.forget(data["frame"])
                del cls.all_open_files[frame_id]

                if cls.has_any_tab_open():
                    cls.selected_tab_frame = False
                cls.mainapp.top_frame.notebook.event_generate("<<TabClosed>>")
                return

    @classmethod
    def has_any_tab_open(cls) -> bool:
        return len(cls.all_open_files) > 0

    @classmethod
    def change_to_next_tab(cls, e=None):
        if not cls.has_any_tab_open():
            return
        notebook: Notebook = cls.mainapp.nametowidget('.!mainframe.!notebook')
        i = notebook.select()
        tab_id = Application.get_tab_id(frame=i)
        list_tabs = list(cls.all_open_files.keys())
        tab_index = list_tabs.index(tab_id)

        new_tab_index = (tab_index + 1)

        if new_tab_index > len(list_tabs)-1:
            new_tab_index = 0

        notebook.select(new_tab_index)
        return 'break'

    @classmethod
    def get_tab_id(cls, frame: str = '', path: str = ''):
        for tab_id, data in cls.all_open_files.items():
            if str(data["frame"]) == str(frame) or str(data["file_path"]) == path:
                return tab_id
        return False

