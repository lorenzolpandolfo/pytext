import os.path
from dataclasses import dataclass


@dataclass
class Application:
    mainapp : None
    selected_tab_frame : None
    mode    : str = "view"

    @classmethod
    def set_mode(cls, arg:str):
        cls.mode = arg
    
    @classmethod
    def get_mode(cls):
        return cls.mode
    
    @classmethod
    def switch_mode(cls, forced_set: str = ''):
        cls.mode = forced_set if forced_set else "view" if cls.mode == "insert" else "insert"
        cls.mainapp.bottom_frame.mode.configure(text=cls.mode)
        state = "disabled" if cls.mode == "view" else "normal"

        cls.selected_tab_frame.textbox.configure(state=state)
        print(cls.selected_tab_frame.textbox)
        cls.mainapp.bottom_frame.command.configure(text="")

    @classmethod
    def set_current_file(cls, path):
        cls.mainapp.file_name = path
        cls.mainapp.bottom_frame.output.configure(text=path)
