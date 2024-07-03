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
        new_window.title("Rename")
        new_window.grid_rowconfigure(1, weight=1)

        sel_file_name = f_exp.get_current_line_content().strip()
        sel_file_path = os.path.join(f_exp.path, sel_file_name)

        label = tk.Label(new_window, text=f"Rename {sel_file_name} to:")

        textarea = tk.Text(new_window, height=14)
        textarea.insert("insert", sel_file_name)

        textarea.grid(row=1, column=0, sticky="ew")
        label.grid(row=0, column=0)

        button = tk.Button(new_window, text="Confirm", command=lambda: rename())
        button.grid(row=2, column=0)
        textarea.bind("<Return>", lambda _: rename())

        textarea.focus_set()
        textarea.tag_add("sel", "1.0", "end")

    @staticmethod
    def _rename_file(file_to_rename_path: str, new_file_title: str):
        new_file_path = os.path.join(os.path.dirname(file_to_rename_path), new_file_title)
        os.rename(file_to_rename_path, new_file_path)
