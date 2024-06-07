import os.path
from dataclasses import dataclass

@dataclass
class Application:
    mainapp:str
    mode:str = "view"

    @classmethod
    def set_mode(cls, arg:str):
        cls.mode = arg
    
    @classmethod
    def get_mode(cls):
        return cls.mode
    
    @classmethod
    def switch_mode(cls):
        cls.mode = "view" if cls.mode == "insert" else "insert"
        cls.mainapp.bottom_frame.mode.configure(text=cls.mode)
        state = "disabled" if cls.mode == "view" else "normal"
        cls.mainapp.main_frame.textbox.configure(state=state)
        cls.mainapp.bottom_frame.command.configure(text="")

    @classmethod
    def set_current_file(cls, path):
        cls.mainapp.file_name = path
        cls.mainapp.bottom_frame.output.configure(text=path)

    # def switch_mode(self):
    #     self.mode = "view" if self.mode == "insert" else "insert"
    #     self.bottom_frame.mode.configure(text=self.mode)

    #     Application.set_mode(self.mode)

    #     state = "disabled" if self.mode == "view" else "normal"
    #     self.main_frame.textbox.configure(state=state)

    #     self.bottom_frame.command.configure(text="")