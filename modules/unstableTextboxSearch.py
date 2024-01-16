from customtkinter import (
    CTk, 
    CTkTextbox,
    CTkFont
)
from modules.localSuggestion import LocalSuggestion

class TextBoxBindings(LocalSuggestion):
    def __init__(self,
        master: any,
        width: int = 200,
        height: int = 200,
        corner_radius: int | None = None,
        border_width: int | None = None,
        border_spacing: int = 3,
        bg_color: str | tuple[str,str] = "transparent",
        fg_color: str | tuple[str,str] | None = None,
        border_color: str | tuple[str,str] | None = None,
        text_color: str | None = None,
        scrollbar_button_color: str | tuple[str,str] | None = None,
        scrollbar_button_hover_color: str | tuple[str,str] | None = None,
        font: tuple | CTkFont | None = None,
        activate_scrollbars: bool = True,
        **kwargs):        

        super().__init__(master, width, height, corner_radius, border_width, border_spacing, bg_color, fg_color, border_color, text_color, scrollbar_button_color, scrollbar_button_hover_color, font, activate_scrollbars, **kwargs)

        # Defining closest characters
        # Use r"" (raw string), no need to use scape chars.
        self._left_chars: str   = r"}])"
        self._right_chars: str  = r"{[("
        self._common_chars: str = r".,;:+-@#$"

        # Creating bindings
        self._textbox.bind("<Control-Left>", self._on_ctrl_left)
        self._textbox.bind("<Control-Right>", self._on_ctrl_right)

    def search_left(self, start_index: str, group: str | list) -> str | None:
        """Searches for a group element and returns index of first occurance."""

        # No action if first index reached.
        if start_index == "1.0":
            return "1.0"

        # Check from the given index
        prev_index = start_index
        while char:=self.get(prev_index):
            if char in group:
                return prev_index
            else:
                # Going one character back
                prev_index = self.index(f"{prev_index} -1c")
                if prev_index == "1.0":
                    return prev_index

    def search_right(self, start_index: str, group: str | list) -> str | None:
        """Searches for a group element and returns index of first occurance."""

        current_line = self.get("insert linestart","insert lineend")
        max_column_in_current_line = len(current_line)

        # Check from the given index
        next_index = start_index

        while char:=self.get(next_index):
            # in case of the line end, cursor will stop
            print(next_index)
            if (int(self.index("insert").split(".")[1])) < max_column_in_current_line:
                return f"{self.index("insert").split(".")[0]}.{max_column_in_current_line}"
            
            # in this case, if you go to right but the next char is a newline, you cursor go to the newline first char
            elif int(self.index("insert").split(".")[0]) < int(next_index.split(".")[0]):
                return next_index

            elif char in group:
                return next_index
            else:
                # Going one character ahead
                next_index = self.index(f"{next_index} +1c")


    def _on_ctrl_left(self, event=None):
        # Getting current index
        current_index = self.index("insert")

        # Getting index of most left selected char
        index = self.search_left(current_index, group=self._left_chars + self._common_chars)

        # Index should not be first (no left exist in this case)
        if index and (index != "1.0"):
            index = self.index(index + " +1c")
            if current_index != index:
                self.mark_set("insert", index)
                return "break" # Prevent default action

    def _on_ctrl_right(self, event=None):
        # Getting current index
        current_index = self.index("insert")

        # Getting index of most right selected char
        index = self.search_right(current_index, group=self._right_chars + self._common_chars)

        # Someting it may return `None`
        if index:
            if current_index != index:
                self.mark_set("insert", index)
                return "break" # Prevent default action
        
        
        
if __name__ == "__main__":
    app = CTk()
    app.geometry("500x350")
    app.grid_columnconfigure(0, weight=1)
    app.grid_rowconfigure(0, weight=1)

    text_box = TextBoxBindings(app, font=CTkFont(size=20))
    text_box.grid(sticky="nsew")

    app.mainloop()
