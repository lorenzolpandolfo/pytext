from customtkinter import CTkFrame, CTkFont, CTkLabel
import os
from modules.widgets.text import Lefttext, Maintext
from modules.ImageManager import ImageManager


class LeftFrame(CTkFrame):
    """ Contains the line counter. """
    def __init__(self, master, font:CTkFont):
        super().__init__(master)

        self.__grid_setup__()
        self.font = font
        
        self.theme_mode = master.theme_mode
        self.theme = master.theme
        self.mode = master.mode

        self.terminal_dir = os.path.join(master.terminal_dir, os.path.dirname(master.file_name))

        self.__load_theme__()
        self.configure(bg_color=self.bg_color, fg_color=self.fg_color)


    def __grid_setup__(self):
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)


    def __load_theme__(self):
        dark = "_dark" if self.master.theme_mode == "dark" else ""
        self.bg_color = self.master.theme["frames"]["left"][f"bg{dark}"]
        self.fg_color = self.master.theme["frames"]["left"][f"fg{dark}"]


    def create_textbox(self, row:int = 0, column:int = 0):
        self.textbox = Lefttext(self, font=self.font)
        # self.textbox.configure(bg_color=self.bg_color, fg_color=self.fg_color)
    
    def hide_textbox(self):
        if self.textbox.winfo_ismapped():
            self.textbox.grid_forget()
    
    def show_textbox(self):
        if not self.textbox.winfo_ismapped():
            self.textbox.grid(row=0, column=0, sticky="nsew")
            self.textbox.open_directory(self.terminal_dir)

    
class BottomFrame(CTkFrame):
    """Contains the outputs labels."""
    def __init__(self, master):
        super().__init__(master)
        self.__load_theme__()
        self.configure(bg_color=self.bg_color, fg_color=self.fg_color)

    def __load_theme__(self):
        dark = "_dark" if self.master.theme_mode == "dark" else ""
        self.bg_color = self.master.theme["frames"]["bottom"][f"bg{dark}"]
        self.fg_color = self.master.theme["frames"]["bottom"][f"fg{dark}"]

        
    def create_widgets(self, output:str):
        self.mode = CTkLabel(self, text=self.master.mode, justify="center", bg_color=self.bg_color, fg_color=self.fg_color, font=self.master.gui_font)
        self.mode.grid(row=1, column=0, columnspan=2)

        self.command = CTkLabel(self, text="", justify="left", bg_color=self.bg_color, fg_color=self.fg_color, font=self.master.gui_font)
        self.command.grid(row=2, column=1, sticky="e")

        self.output = CTkLabel(self, text=output.replace("\\", "/"), bg_color=self.bg_color, fg_color=self.fg_color, padx=10, justify="left", font=self.master.gui_font)
        self.output.grid(row=2, column=0)

        self.grid_columnconfigure(1, weight=1)

    def load_icons(self):
        self.branch_image = ImageManager.get_image("branch", (20, 22))
    
    def create_branch_icon(self, branch:str):
        if "\n" in branch:
            branch = branch.replace("\n", "")

        self.branch = CTkLabel(self, image=self.branch_image, text=branch, justify="left", compound="left", font=self.master.gui_font, padx=10)
        self.branch.grid(row=2, column=2, sticky="e")

    
    def destroy_branch_icon(self):
        print("Destruindo")
        try:
            self.branch.destroy()
        except AttributeError:
            pass


class MainFrame(CTkFrame):
    """It is the main frame that contains the Maintext instance."""
    def __init__(self, master, font:CTkFont):
        super().__init__(master)
        self.font = font
        
        self.theme_mode = master.theme_mode
        self.theme = master.theme
        self.mode = master.mode


        self.__grid_setup__()
        self.__load_theme__()


    def __load_theme__(self):
        dark = "_dark" if self.theme_mode == "dark" else ""
        self.bg_color = self.theme["frames"]["left"][f"bg{dark}"]
        self.fg_color = self.theme["frames"]["left"][f"fg{dark}"]
        

    def create_textbox(self, row:int = 0, column:int = 0):
        self.textbox = Maintext(self, font=self.font)
        self.textbox.grid(row=row, column=column, sticky="nsew")
        #self.textbox.configure(bg_color=self.bg_color, fg_color=self.bg_color)
        self.master.update()
        self.textbox.focus_set()

    def __grid_setup__(self):
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
