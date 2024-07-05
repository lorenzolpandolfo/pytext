import os
import tkinter as tk

from modules.Application import Application
from modules.FileLoader import FileLoader


class Renamer:

    @staticmethod
    def _rename(file_path, t, window):
        f_exp = Application.mainapp.left_frame.textbox

        Renamer._rename_file(
            file_to_rename_path=file_path,
            new_file_title=(t.get("1.0", "end-1c")),
            open_it=True
        )
        f_exp.open_directory(os.path.dirname(file_path))
        window.destroy()
        return "break"

    @staticmethod
    def create_rename_window(custom_file: dict | bool = False):
        f_exp = Application.mainapp.left_frame.textbox

        sel_file_name = f_exp.get_current_line_content().strip()
        sel_file_path = os.path.join(f_exp.path, sel_file_name)
        window_title = "Rename file"
        window_description = f"rename {sel_file_name} to:"

        if custom_file:
            sel_file_name = custom_file["file_title"]
            sel_file_path = custom_file["file_path"]
            window_title = "Save as"
            window_description = f"save {sel_file_name} as:"

        new_window = tk.Toplevel(Application.mainapp)
        new_window.title(window_title)
        new_window.geometry("400x150")
        new_window.resizable(False, False)

        new_window.grid_rowconfigure(0, weight=1)
        new_window.grid_columnconfigure(0, weight=1)

        frame = tk.Frame(new_window, padx=15, pady=15)
        frame.grid(row=0, column=0, sticky="nsew")
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_rowconfigure(2, weight=1)
        frame.grid_columnconfigure(0, weight=1)

        label = tk.Label(frame, text=window_description)

        textarea = tk.Text(frame, height=1, width=10)
        textarea.insert("insert", sel_file_name)

        button = tk.Button(frame, text="Confirm", command=lambda: Renamer._rename(sel_file_path, textarea, new_window))

        textarea.bind("<Return>", lambda _: Renamer._rename(sel_file_path, textarea, new_window))
        new_window.bind("<Escape>", lambda _: new_window.destroy())

        textarea.focus_set()
        textarea.tag_add("sel", "1.0", "end")

        label.grid(row=0, column=0)
        textarea.grid(row=1, column=0, sticky="nsew")
        button.grid(row=2, column=0)

    @staticmethod
    def _rename_file(file_to_rename_path: str, new_file_title: str, open_it: bool = False):
        if not file_to_rename_path or not new_file_title:
            return False

        if not os.path.isfile(file_to_rename_path):
            return False

        # check if new file name has extension. Else, add the older extension
        _, new_file_ext = os.path.splitext(new_file_title)
        if new_file_ext == '':
            _, old_file_ext = os.path.splitext(file_to_rename_path)
            new_file_title += old_file_ext

        new_file_path = os.path.join(os.path.dirname(file_to_rename_path), new_file_title)
        os.rename(file_to_rename_path, new_file_path)
        if open_it:
            FileLoader.open_file(new_file_path)
