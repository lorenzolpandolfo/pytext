from dataclasses import dataclass
from tkinter.font import Font


@dataclass
class FontManager:
    GUI_FONT  = None
    FILE_FONT = None

    @classmethod
    def load_user_font(cls, user_font: dict):
        family    = user_font["family"]
        size      = user_font["text_size"]
        gui_size  = user_font["gui_size"]

        cls.FILE_FONT = Font(family=family, size=size)
        cls.GUI_FONT  = Font(family=family, size=gui_size)
