from customtkinter import CTkTextbox, CTkFont, CTk
from tkinter import Event, END
from typing import Callable
from tkinterdnd2 import *

from json import load as load_json
from re import finditer, MULTILINE
from string import printable, whitespace, punctuation
from customtkinter import set_appearance_mode

import os

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
        activate_scrollbars: bool = False,
        wrap_callable: Callable[..., None] | None = None,
        **kwargs):

        super().__init__(master, width, height, corner_radius, border_width, border_spacing, bg_color, fg_color, border_color, text_color, scrollbar_button_color, scrollbar_button_hover_color, font, activate_scrollbars, **kwargs)

        # Line specific storage
        self._current_line: int = 1
        self._wrap_command      = wrap_callable

        self.drop_target_register(DND_ALL)
        self.dnd_bind(f"<<Drop>>", self.__drop_file_into_textbox__)

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

    def __drop_file_into_textbox__(self, event: str | None = None) -> None:
        self.delete(f"1.0", END)
        try:
            with open(event.data, f"r+", encoding=f"UTF-8") as self.openned_file:
                self.insert(f"1.0", self.openned_file.read())

        except FileNotFoundError: pass


    # Syntax highlight methods

# Declaring indicating variables
        self._groups: dict              = None
        self._colors: dict              = None
        self._syntax_rules_loaded: bool = False
        self._boundary_chars: list      = None

    def _active_syntax_highlighting(self):
        # Binding key stroke event
        self.bind("<KeyRelease>",
                  lambda _: self.after(2, self._highlight_syntax))
        
    def _get_number_indices(self, string: str) -> list[tuple[int, int]]:
        pattern = r'\b\d+\.\d+|\b\d+\b|\.\d+'  # Regular expression for matching integers and floats
        matches = finditer(pattern, string)

        indices = []
        for match in matches:
            indices.append((match.start(), match.end()))

        return indices
    
    def _get_quoted_text_indices(self, string) -> list[tuple[int, int]]:
        pattern = r'(\'\'\'|\"\"\")([\s\S]*?)\1|(\'|\")([\s\S]*?)\3'  # Regular expression for matching quoted text
        matches = finditer(pattern, string)

        indices = []
        for match in matches:
            start = match.start()
            end = match.end()
            indices.append((start, end))

        return indices
    
    def _get_commented_text_indices(self, string) -> list[tuple[int, int]]:
        # Regular expression for matching Python comments
        pattern = r'#.*?$|(\'\'\'|\"\"\")([\s\S]*?)\1'

        matches = finditer(pattern, string, MULTILINE)

        indices = []
        for match in matches:
            start = match.start()
            end = match.end()
            indices.append((start, end))

        return indices

    def _highlight_keywords(self):
        for group, values in self._groups.items():
            for value in values:
                for occurance in self.search_all(value, exact=False if group == "operators" else True):
                    index_start = occurance[0]
                    index_end = occurance[1]

                    # Applying the color tag
                    self.tag_add(group, index_start, index_end)
    
    def _highlight_numbers(self):
        for row, line in enumerate(self.get("1.0", "end").splitlines(), start=1):
            for occurance in self._get_number_indices(line):
                start_index = f"{row}.{occurance[0]}"
                last_index  = f"{row}.{occurance[1]}"
            
                # Applying the color tag
                self.tag_add("numbers", start_index, last_index)
            
    def _highlight_comments(self):
        for row, line in enumerate(self.get("1.0", "end").splitlines(), start=1):
            for occurance in self._get_commented_text_indices(line):
                start_index = f"{row}.{occurance[0]}"
                last_index  = f"{row}.{occurance[1]}"
            
                # Applying the color tag
                self.tag_add("comments", start_index, last_index)

    def _highlight_strings(self):
        for row, line in enumerate(self.get("1.0", "end").splitlines(), start=1):
            for occurance in self._get_quoted_text_indices(line):
                start_index = f"{row}.{occurance[0]}"
                last_index  = f"{row}.{occurance[1]}"
            
                # Applying the color tag
                self.tag_add("strings", start_index, last_index)
    
    def _remove_existing_colors(self):
        # Deleting highlighting tags
        for group, _ in self._colors.items():
            self.tag_remove(group, "1.0", "end")

    def _highlight_syntax(self):
        # Removing all existing colors
        self._remove_existing_colors()

        # Highlighting new entries
        self._highlight_keywords()
        self._highlight_numbers()
        self._highlight_comments()
        self._highlight_strings()

    def _check_boundaries(self, index_start: str, index_end: str):
        before_char = self.get(index_start + " -1c") if index_start.split(".")[1] != "0" else "\n"
        after_char = self.get(index_end)

        if (before_char not in self._boundary_chars) and (after_char not in self._boundary_chars):
            return True
        else:
            return False

    def search_all(self, word: str, exact: bool = True) -> list[tuple[int, int]]:
        """Returns all occurance indices of the word."""
        word_length: int   = len(word)
        initial_index: str = "1.0"
        matches: list      = []

        while match:= self.search(word, initial_index, stopindex="end"):
            row, column = match.split(".")
            last_index  = f"{row}.{int(column) + word_length}"
            initial_index = last_index

            if exact:   # Prevents substring from detection
                if not self._check_boundaries(match, last_index):
                    continue

            matches.append((match, last_index))

        
        return matches
    
    def load_syntax_rules(self, group_file: str, color_file: str):
        with open(group_file, "r") as group:
            with open(color_file, "r") as colors:
                self._groups = load_json(group)
                self._colors = load_json(colors)
        
        # Creating highlighting tags
        for group, color in self._colors.items():                   # This will set colors of all the syntax
            self.tag_config(group, foreground=color)

        # Loading boundary characters
        self._boundary_chars = [char for char in printable 
                                if char not in (whitespace + punctuation)]

        # Allow following at the boundary
        self._boundary_chars.extend(["_"])

        self._syntax_rules_loaded = True

    def active_syntax_highlighting(self):
        if not self._syntax_rules_loaded:
            raise LookupError("Please provide syntax rule files.")
        else:
            self._active_syntax_highlighting()