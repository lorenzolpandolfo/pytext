from customtkinter import CTkTextbox, CTkFont
from tkinter import Event
from typing import Callable

# Standard Solution. Handles all interections well.

class CTkEasyTextBox(CTkTextbox):
    """Updated to know a wrapping is done or not."""
    def __init__(self,
        master: any,
        width: int = 200,
        height: int = 200,
        corner_radius: int | None = None,
        border_width: int | None = None,
        border_spacing: int = 3,
        bg_color: str | tuple[str, str] = "transparent",
        fg_color: str | tuple[str, str] | None = None,
        border_color: str | tuple[str, str] | None = None,
        text_color: str | None = None,
        scrollbar_button_color: str | tuple[str, str] | None = None,
        scrollbar_button_hover_color: str | tuple[str, str] | None = None,
        font: tuple | CTkFont | None = None,
        activate_scrollbars: bool = True,
        wrap_callable: Callable[..., None] | None = None,
        **kwargs):

        super().__init__(master, width, height, corner_radius, border_width, border_spacing, bg_color, fg_color, border_color, text_color, scrollbar_button_color, scrollbar_button_hover_color, font, activate_scrollbars, **kwargs)

        # Line specific storage
        self._current_line: int = 1
        self._wrap_command      = wrap_callable

        # Adding character validation by default
        # Ao ativar aqui, ele confere se a linha atual selecionada é wrapped
        # self.bind("<Key>", lambda _: self._handle_pressed_button())

    def getCursoredExtremes(self) -> (str, str):
        first_index = self.index("insert linestart")
        last_index  = self.index(first_index + " lineend")

        return first_index, last_index
    
    def getCursoredLine(self) -> str:
        return self.index("insert").split(".")[0]

    def _handle_pressed_button(self) -> None:
        def check():
            wrap = self._isWrapped(*self.getCursoredExtremes())
            if wrap:
                if self._wrap_command: self._wrap_command({"line": self.getCursoredLine(), "wrapped_lines": wrap})
            else:
                if self._wrap_command: self._wrap_command({"line": self.getCursoredLine(), "wrapped_lines": 0})

        # Let the character be updated to the text box.
        # Then attempting the checking
        self.after(2, check)

    def getTotalLines(self) -> int:
        """Returns total number of lines in the text box in real time."""
        return self.get("1.0", "end").count("\n")

    def getLines(self) -> list[str]:
        """Returns list of all the lines."""
        return [line for line in self.get(1.0, "end").split("\n") if line != ""]
    
    def getLine(self, line_number: int) -> str:
        """Returns line by line number."""

        # Checking whether `line_number` >= 1 or not.
        if line_number <=0: return ""

        # Getting line's extremes
        first_index = self.index(f"{line_number}.0 linestart")
        last_index  = self.index(first_index + " lineend")

        return self.get(first_index, last_index)
    
    def addNewline(self, line: str = ""):
        """Adds new line."""
        # Adding new line character (Enter) at the end of the line
        self.insert("end", line + "\n", tags=f"line{self._current_line}")
        self._current_line = self._current_line + 1

        # Updating the master to the current
        self.nametowidget(".").update()

    def getLineExtremes(self, line_number: int) -> (float, float):
        """Returns first and last characters' indeces of a line."""
        first_index = self.index(f"{line_number}.0 linestart")
        last_index  = self.index(first_index + " lineend")

        return first_index, last_index
    
    def _isWrapped(self, first_index: str, last_index: str):
        first_position, last_positon = self.bbox(first_index)[1], self.bbox(last_index)[1]
        if first_position == last_positon:
            return False
        else:
            difference = last_positon - first_position
            constant   = self.bbox(last_index)[3]         # Height of the line
            lines      = difference/constant 

            return int(lines)
        
    def isWrapped(self, line_number: int) -> bool | int:
        # O line_number é absoluto e precisa ser visivel
        """Returns `False` if line is not wrapped else number of the wrapped lines."""
        if line_number <= 0: return False

        # Updating the master to the current
        self.nametowidget(".").update()

        # Getting the extremes of the line
        first_index, last_index = self.getLineExtremes(line_number)

        return self._isWrapped(first_index, last_index)