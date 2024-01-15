from customtkinter import (
    CTk,
    CTkTextbox,
    CTkFont
)
from modules.CTkEasyTextBox import CTkEasyTextBox
from customtkinter import set_appearance_mode

from string import ascii_letters, digits
from string import punctuation, whitespace
from tkinter import Event
from re import findall, escape

class LocalSuggestion(CTkEasyTextBox):
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
        **kwargs):
        super().__init__(master, width, height, corner_radius, border_width, border_spacing, bg_color, fg_color, border_color, text_color, scrollbar_button_color, scrollbar_button_hover_color, font, activate_scrollbars, **kwargs)

        # An appropriate color in both the modes
        SUGGESTED_WORD_COLOR = "#6e7681"

        # Words which are allowed at the boundaries of the word
        self._word_acceptable_chars: str = whitespace + punctuation

        # Initializing a list which will contain current suggestion details
        self._current_suggested: list[str, tuple[str, str], str] = []

        # Defining suggested tag to apply to the suggestion text
        self.tag_config("suggested", foreground=SUGGESTED_WORD_COLOR)

        # Binding key detection
        self.bind("<KeyRelease>", 
                  lambda event: self.after(1, lambda: self._on_type(event)))
        
        # Suggestion accepting methods. Standard is `Tab`.
        self.bind("<Button-1>", self._on_tab)           # On any click if suggestion is appeared
        self._textbox.bind("<Tab>", self._on_tab)       # On pressing `tab` key if suggestion is appeared
        self._textbox.bind("<Return>", self._on_tab)    # On pressing `Enter` key if suggestion is appeared
    
    def _extract_words_with_prefix(self, text, prefix) -> list[str]:
        """Lists all the words starts with given prefix. Will be used in suggestions"""

        # Define a regex pattern to match words starting with the specified prefix
        pattern = r'\b' + escape(prefix) + r'\w*\b'

        # finding all matches of the pattern in the text
        words = findall(pattern, text)

        return words
    
    def _get_current_spelling(self) -> list[str, tuple[int, int]]:
        """Returns current spelling user being typed."""

        # Getting current cursored index as the last index of the spelling
        last_index  = self.index("insert")
        row, column = last_index.split(".")

        # Setting first index as empty and 
        # stop index as a first character of the line
        index, stop = "", f"{row}.0"
        
        if column == "0":
            return ["", (stop, last_index)]
        
        # Checking where the word boundary character will be found
        for char in self._word_acceptable_chars:
            # Searching in backward direction from the current index
            index = self.search(char, index=last_index, stopindex=stop, backwards=True)

            # If any boundary character found, stop finding
            if index: break

        # Next character to the boundary char. If None, set to the first character to the line
        index = (index + " +1c") if index else stop 
        
        # Returning the result in the form: [spelling, (start_index, end_index)]
        return [self.get(index, last_index), (index, last_index)]
    
    def _get_suggestion(self, prefix: str) -> str:       
        """Returns direct suggestion as string."""           
        for line in [line for line in self.get("1.0", "end").split("\n") if line != ""]:
            words = self._extract_words_with_prefix(line, prefix)
            if words:
                return words[0]

        return ""
        
    def _place_suggested(self, suggestion: str):
        """Make the suggestion appeared."""
        # Getting the last index of the current spelling typed by user
        _, last_index = self._current_suggested[1]

        # Inserting the suggestion next to the user typed 
        # word (or spelling) removing the typed pard from the suggested word
        self.insert(last_index, text=suggestion[len(self._current_suggested[0]):], tags="suggested")

        # Setting cursor to the user position again
        self.mark_set("insert", index=self._current_suggested[2])

    def _clear_recent_suggestion(self):
        """Frees suggestion store"""
        self._current_suggested.clear()
        self._current_suggested = []

    def _remove_placed_suggestion(self):
        """Handles if user declines the suggestion"""

        # Checking if any missed. (This case may happen in pasting text.)
        ranges = self.tag_ranges("suggested")

        if ranges:
            # Removing the tag
            start_index, end_index = ranges 
            self.tag_remove("suggested", start_index, end_index)

            # Removing the text
            current_position = self.index("insert")
            self.delete(current_position, end_index)

        # Clearing at all
        self._clear_recent_suggestion()

    def _pull_suggerstion(self):
        """When user accepts the suggestion"""

        # Withdrawing suggestion color
        start_index, end_index = self.tag_ranges("suggested")
        self.tag_remove("suggested", start_index, end_index)

        # Set cursor to the next to the suggested word which was accepted
        self.mark_set("insert", end_index)

        # Freeing suggestion storage
        self._clear_recent_suggestion()

    def _on_tab(self, e=None):
        """If suggestion is appeared."""

        if self._current_suggested:
            # Finalize the suggestion
            self._pull_suggerstion()

            # Discarding THIS key (can be 'Tab' or 'Enter').
            return "break"  # Prevents inserting `tab` or other new key.
    
    def _on_type(self, event: Event):
        """Handles every key stroke by the user."""

        # If the key is an alphabet or digit
        if event.keysym in (ascii_letters + digits):
            # Getting current user typed spelling for suggestion
            current_word = self._get_current_spelling()

            # Checking if suggestion is already placed, remove that.
            if self._current_suggested:
                self._remove_placed_suggestion()

            # If valid spelling typed
            if word:= current_word[0]:
                suggestion   = self._get_suggestion(word)

                # If suggestion does not equal to spelling itself
                if suggestion and (word != suggestion):   
                    # If suggestion is not only one character littler than the spelling                     
                    if abs(len(word) - len(suggestion)) > 1:
                        # Storing `current_word` list in  `_current_suggested`
                        self._current_suggested = current_word

                        # Appending the current index to the suggested
                        self._current_suggested.append(self.index("insert"))

                        # Transferring the "current spelling" and "its indices" with "cursor index"
                        # to the suggestion placing mechanism
                        self._place_suggested(suggestion)

        else:
            # Checking if suggestion is already placed, remove that.
            if self._current_suggested:
                # Preventing deletion on key 'Shift'
                if "Shift" not in event.keysym:
                    self._remove_placed_suggestion()
