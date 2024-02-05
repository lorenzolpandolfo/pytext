import os

import customtkinter as ctk
from tklinenums import TkLineNumbers

import pygments
from pygments.lexers import get_lexer_by_name
# from pygments.token import Token

from modules.UserConfig     import UserConfig
from modules.FontManager    import FontManager
from modules.ImageManager   import ImageManager
from modules.SyntaxColors   import SyntaxColors
from modules.FileManager    import FileManager
from modules.ThemeManager   import ThemeManager
from modules.tklinenums     import TkLineNumbers


class MainApp(ctk.CTk):
    def __init__(self, terminal_dir:str, file_name:str):
        super().__init__()

        self.terminal_dir  = terminal_dir
        self.file_name     = file_name
        self.theme_mode = self._get_appearance_mode()

        self.__load_user_config__()   
        self.__load_user_font__()
        self.__load_user_theme__()
        self.__create_gui__()

        if self.file_name:
            self.__load_argv_file__()
        self.__enable_binds__()

      
    def __load_user_config__(self):
        self.config = UserConfig.get_user_config()
    
    def __load_user_font__(self):
        font = self.config["font"]
        loader = FontManager.load_user_font(font)
        
        if isinstance(loader, int):
            print(f"Error: could not load font '{font['title']}'. Loading default font instead.")
            self.font     = ctk.CTkFont("Consolas", 26)
            self.gui_font = ctk.CTkFont("Consolas", 17)
        else:
            self.font, self.gui_font = loader

    def __load_user_theme__(self):
        self.theme = ThemeManager.get_user_theme()


    def __create_gui__(self):
        self.__create_window__()
        self.__configure_grids__()
        self.__create_frames__()
        self.__create_widgets__()

    def __create_window__(self):
        self.title("The Pytext Editor Refactored")
        self.geometry(self.config["window_size"])
        self.resizable(True, True)

    def __configure_grids__(self):
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)

        self.grid_columnconfigure(0, weight=0, minsize=60)
        self.grid_columnconfigure(1, weight=1)

    def __create_frames__(self):
        self.bottom_frame = BottomFrame(self)
        self.bottom_frame.grid(row=1, column=0, sticky="we", columnspan=2, rowspan=2)

        self.main_frame = MainFrame(self, self.font)
        self.main_frame.grid(row=0, column=1, sticky="nsew")

        self.left_frame = LeftFrame(self, self.font)
        self.left_frame.grid(row=0, column=0, sticky="nsew")
        
    def __create_widgets__(self):
        self.main_frame.create_textbox()
        self.main_frame.textbox.create_line_counter(self.left_frame)
        self.main_frame.textbox.set_tab_width(tabwidth=self.config["tab_width"])

        self.left_frame.create_textbox()
        
        self.bottom_frame.create_widgets(output=(self.file_name if self.file_name else "Welcome to Pytext refactored"))
        self.bottom_frame.load_icons()


    def __load_argv_file__(self):
        full_path = os.path.join(self.terminal_dir, self.file_name)

        self.main_frame.textbox.open_file(full_path)

        if FileManager.check_if_repository(full_path):
            self.bottom_frame.create_branch_icon(FileManager.get_git_branch(full_path))
        # else:
        #     self.bottom_frame.destroy_branch_icon()


    def __enable_binds__(self):
        self.bind("<Key>", lambda e: self.bind_dealing(e))
    
    def bind_dealing(self, event = None):
        focus = str(self.focus_get())
        left_textbox_visible = self.left_frame.textbox.winfo_ismapped()

        if left_textbox_visible:
            if event.keysym == "Return":
                file_name = self.left_frame.textbox.get_current_line_content().strip()
                if file_name[0] == "▼":
                    self.left_frame.textbox.updir()
                    return self.left_frame.textbox.open_directory(self.left_frame.textbox.path)
                
                elif file_name[0] == "/":
                    file_name = file_name[1:]

                content = os.path.join(self.left_frame.textbox.path, file_name)

                if os.path.isdir(content):
                    return self.left_frame.textbox.open_directory(content)
                else:
                    # contar quantos diretorios tem antes e ir salvando a posicao do cursor pra retomar
                    if self.main_frame.textbox.open_file(content):
                        self.main_frame.textbox.focus_set()

            

        if event.keysym == "Escape" and left_textbox_visible:
            self.left_frame.hide_textbox()
            self.main_frame.textbox.focus_set()
        
        elif (event.state & 0x4) and event.keysym == "f":
            if left_textbox_visible:
                if "leftframe" in focus:
                    print("??")
                    self.left_frame.hide_textbox()
                    self.main_frame.textbox.focus_set()
                else:
                    self.left_frame.textbox.focus_set()
            else:
                self.left_frame.show_textbox()
                self.left_frame.textbox.focus_set()



class LeftFrame(ctk.CTkFrame):
    """Contains the line counter."""
    def __init__(self, master, font:ctk.CTkFont):
        super().__init__(master)

        self.__grid_setup__()
        self.font = font
        self.theme_mode = master.theme_mode
        self.theme = master.theme
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

    
class BottomFrame(ctk.CTkFrame):
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
        self.mode = ctk.CTkLabel(self, text="View", justify="center", bg_color=self.bg_color, fg_color=self.fg_color, font=self.master.gui_font)
        self.mode.grid(row=1, column=0, columnspan=2)

        self.command = ctk.CTkLabel(self, text="99d", justify="left", bg_color=self.bg_color, fg_color=self.fg_color, font=self.master.gui_font)
        self.command.grid(row=2, column=1, sticky="e")

        self.output = ctk.CTkLabel(self, text=output.replace("\\", "/"), bg_color=self.bg_color, fg_color=self.fg_color, padx=10, justify="left", font=self.master.gui_font)
        self.output.grid(row=2, column=0)

        self.grid_columnconfigure(1, weight=1)

    def load_icons(self):
        self.branch_image = ImageManager.get_image("branch", (20, 22))
    
    def create_branch_icon(self, branch:str):
        if "\n" in branch:
            branch = branch.replace("\n", "")

        self.branch = ctk.CTkLabel(self, image=self.branch_image, text=branch, justify="left", compound="left", font=self.master.gui_font, padx=10)
        self.branch.grid(row=2, column=2, sticky="e")

    
    def destroy_branch_icon(self):
        print("Destruindo")
        try:
            self.branch.destroy()
        except AttributeError:
            pass


class MainFrame(ctk.CTkFrame):
    """It is the main frame that contains the Maintext instance."""
    def __init__(self, master, font:ctk.CTkFont):
        super().__init__(master)
        self.font = font
        self.theme_mode = master.theme_mode
        self.theme = master.theme

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



class Generaltext(ctk.CTkTextbox):
    """Includes methods that Maintext and Lefttext use"""
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

    def enable_auto_highlight_line(self):
        self.bind("<Key>", lambda _: self.after_idle(lambda: self.highlight_selected_line()))
        
    def highlight_selected_line(self, event=None):
        line_start = int(self.index("insert").split(".")[0])
        self.tag_remove("current_line_color", "1.0", "end")
        self.tag_add("current_line_color", f"{line_start}.0", f"{line_start + 1}.0")
        self.tag_config("current_line_color", background=self.selected_line_color)

    def load_theme(self, child):
        dark = "_dark" if self.master.theme_mode == "dark" else ""
        child = str(child)

        widget = "main_textbox" if "maintext" in child else "left_textbox"

        bg_color            = self.master.theme["widgets"][widget][f"bg{dark}"]
        selected_line_color = self.master.theme["widgets"][widget][f"selected_line{dark}"]
        font_color          = self.master.theme["widgets"][widget][f"font{dark}"]
        exp_dir_color       = self.master.theme["explorer"][f"dir{dark}"]
        exp_file_color      = self.master.theme["explorer"][f"file{dark}"]
        exp_curdir_color    = self.master.theme["explorer"][f"curdir{dark}"]

        return (bg_color, selected_line_color, font_color, exp_dir_color, exp_file_color, exp_curdir_color)

    def write_file_content(self, content:str | tuple, mark_set:str = "insert"):
        """ Directly write a file content. """
        self.delete("1.0", "end")
        self.insert("1.0", content)
        if mark_set:
            self.mark_set(mark_set, "1.0")


    def write_directory_content(self, content:tuple, colors:tuple, mark_set:str = "insert"):
        """ Write files from a directory. Deals with directories colors. """
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        self.configure(state="normal")

        raw_content = content[0]
        formatted_content = content[1]

        self.delete("1.0", "end")
        self.insert("1.0", formatted_content)
        
        # adding colors to other directories inside of the content
        for i, file in enumerate(raw_content.split("\n")):
            full_path = os.path.join(self.master.terminal_dir, file)

            if os.path.isdir(full_path):
                self.tag_add("directory_color", f"{i + 2}.0", f"{i + 3}.0")
                self.tag_config("directory_color", foreground=colors[0])
            
            elif os.path.isfile(full_path):
                self.tag_add("file_color", f"{i + 2}.0", f"{i + 3}.0")
                self.tag_config("file_color", foreground=colors[1])
        if mark_set:
            self.mark_set(mark_set, "1.0")
        
        self.configure(state="disabled")


    
    def open_file(self, full_path:str):
        """ Open a file through a directory and title. Then, write it. """
        content = FileManager.open_file(full_path)
        if content:
            self.write_file_content(content)
        else:
            return False

    def open_directory(self, dir_path:str, auto_write:bool = True):
        content = FileManager.open_directory(dir_path)
        if content:
            self.path = dir_path

            if auto_write:
                self.write_directory_content(content, colors=(self.exp_dir_color, self.exp_file_color, self.exp_curdir_color))

    def set_tab_width(self, tabwidth:int):
        self.configure(tabs=self.cget("font").measure(" ") * tabwidth)

    def focus_set(self):
        super().focus_set()
        self.highlight_selected_line()

    def get_current_line_content(self):
        line_start = int(self.index("insert").split(".")[0])
        return self.get(f"{line_start}.0", f"{line_start + 1}.0")



class Maintext(Generaltext):
    """Represents the main textbox of Pytext."""
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        super().enable_auto_highlight_line()

        self.bg_color, self.selected_line_color, self.font_color, self.exp_dir_color, self.exp_file_color, self.exp_curdir_color = super().load_theme(self)
        self.configure(bg_color=self.bg_color, fg_color=self.bg_color)

        self._lexer = pygments.lexers.PythonLexer
        self._colors = SyntaxColors.get_syntax_colors()
        #self._enable_binds_()

    def _enable_binds_(self):
            self.bind("<Key>", lambda e: self.after_idle(lambda: self.__bind_dealing__(e)))

    def __bind_dealing__(self, event):
        pass
            
    def create_line_counter(self, master):
        def load_line_counter_theme() -> tuple:
            dark = "_dark" if self.master.theme_mode == "dark" else ""
            bg_color = self.master.theme["widgets"]["line_counter"][f"bg{dark}"]
            font_color = self.master.theme["widgets"]["line_counter"][f"font{dark}"]
            return (bg_color, font_color)
        bg_color, font_color = load_line_counter_theme()

        #self.update()
        self._line_counter = TkLineNumbers(master, self, justify="right", colors=(font_color, bg_color),tilde="~", bd=0)
        self._line_counter.grid(row=0, column=1, sticky="nsew", pady=(6 * (self._get_widget_scaling()) + 0.5,0))
        self.__enable_auto_redraw__()

    def __enable_auto_redraw__(self):
        self.bind("<Key>", lambda e: self.after_idle(self._line_counter.redraw), add=True)
        # self.bind("<KeyRelease>", lambda e: self.highlight_line())
        # self.bind("<Control-v>", lambda e: self.highlight_all())
        # self.bind("<Prior>", lambda e: self.highlight_all())

        # this yscrollcommand also auto resizes pytext to the current resolution
        self.configure(yscrollcommand=self.__y_scroll_command__)
    
    def __y_scroll_command__(self, *scroll_pos:tuple):
        self._y_scrollbar.set(scroll_pos[0], scroll_pos[1])
        self._line_counter.redraw()

    def highlight_line(self, lexer="python", line_num:str=""):
        line_num = int(self.index("insert").split(".")[0]) if line_num == "" else line_num

        #for tag in self.tag_names(index=None):
        #    if tag.startswith("Token"):
        #        self.tag_remove(tag, "1.0", "end")
        #        self.tag_delete(tag)
        #        print(tag, " removida")
                
        lexer = get_lexer_by_name(lexer)
        content = self.get(f"{line_num}.0 linestart", f"{line_num}.0 lineend")
        tokens = list(pygments.lex(content, lexer))
        
        for tag in self.tag_names("insert"):
            if tag != "sel":
                # print(tag)
                self.tag_remove(tag, "insert linestart", "insert lineend")

        start_col = 0
        for (token, text) in tokens:
            token = str(token)

            end_col = start_col + len(text)
            if token not in ["Token.Text.Whitespace", "Token.Text"]:
                self.tag_add(token, f"{line_num}.{start_col}", f"{line_num}.{end_col}")
                #print(f"{line_num}.{start_col}", f"{line_num}.{end_col}")
                if token.split(".")[1] in self._colors:
                    self.tag_config(token, foreground=self._colors[token.split(".")[1]])
            start_col = end_col

        self.update()
        all = self.get("1.0", "end")
        num_lines = all.count("\n")
        
        first_line = int(self.index("@0,0").split(".")[0])
        last_line = int(
            self.index(f"@0,{self.winfo_height()}").split(".")[0]
        )

        for i in range(first_line, last_line):
            self.highlight_line("python", i)


class Lefttext(Generaltext):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        super().enable_auto_highlight_line()

        self.bg_color, self.selected_line_color, self.font_color, self.exp_dir_color, self.exp_file_color, self.exp_curdir_color = super().load_theme(self)
        self.configure(bg_color=self.bg_color, fg_color=self.bg_color, state="disabled")
    
    def updir(self):
        self.path = os.path.dirname(self.path)



if __name__ == "__main__":
    import sys
    file_name = sys.argv[1] if len(sys.argv) > 1 else ""
    # check if this is not problematic. I think that it is not
    file_name = file_name[2:] if file_name[:2] == ".\\" else file_name
    if_argv_is_file = os.path.isfile(os.path.join(os.getcwd(), file_name))
    app = MainApp(terminal_dir=os.getcwd(), file_name=file_name) if if_argv_is_file else MainApp(terminal_dir=os.getcwd(), file_name="")
    app.mainloop()
