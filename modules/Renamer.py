import os
import tkinter as tk

from modules.Application import Application


class Renamer:
    @staticmethod
    def create_rename_window():
        f_exp = Application.mainapp.left_frame.textbox

        def rename():
            Renamer._rename_file(
                sel_file_path, textarea.get("1.0", "end-1c")
            )
            f_exp.open_directory(os.path.dirname(sel_file_path))
            new_window.destroy()
            return "break"

        new_window = tk.Toplevel(Application.mainapp)
        new_window.title("Rename file")
        new_window.geometry("400x150")
        new_window.resizable(False, False)

        new_window.grid_rowconfigure(0, weight=1)
        new_window.grid_columnconfigure(0, weight=1)

        frame = tk.Frame(new_window, padx=15, pady=15)
        frame.grid(row=0, column=0, sticky="nsew")
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_rowconfigure(2, weight=1)
        frame.grid_columnconfigure(0, weight=1)

        sel_file_name = f_exp.get_current_line_content().strip()
        sel_file_path = os.path.join(f_exp.path, sel_file_name)

        label = tk.Label(frame, text=f"Rename {sel_file_name} to:")

        textarea = tk.Text(frame, height=1, width=10)
        textarea.insert("insert", sel_file_name)

        button = tk.Button(frame, text="Confirm", command=lambda: rename())

        textarea.bind("<Return>", lambda _: rename())
        new_window.bind("<Escape>", lambda _: new_window.destroy())

        textarea.focus_set()
        textarea.tag_add("sel", "1.0", "end")

        label.grid(row=0, column=0)
        textarea.grid(row=1, column=0, sticky="nsew")
        button.grid(row=2, column=0)

    @staticmethod
    def _rename_file(file_to_rename_path: str, new_file_title: str):
        _, ext = os.path.splitext(new_file_title)
        if ext == '':
            _, old_ext = os.path.splitext(file_to_rename_path)
            new_file_title += old_ext

        new_file_path = os.path.join(os.path.dirname(file_to_rename_path), new_file_title)
        os.rename(file_to_rename_path, new_file_path)
