import os
import tkinter as tk
from modules.Application import Application
import re


class CommandManager:
    @classmethod
    def command_dealing(cls, event):
        focus = str(Application.mainapp.focus_get())
        if ("mainframe" in focus) and (Application.get_mode() == "view"):
            cur_command = Application.mainapp.bottom_frame.command.cget("text")
            cur_command_chars = ''.join(re.findall(r'[a-zA-Z]+', cur_command))

            if (cur_command and event.keysym == "Escape") or (len(cur_command_chars) >= 3):
                return True

            if event.char.isalpha() or event.char.isdigit():
                command = CommandManager.add_char_to_command(cur_command, event.char)
                Application.mainapp.bottom_frame.command.configure(text=command)
                return CommandManager.validate_command(command)

    @classmethod
    def add_char_to_command(cls, cur_command, char):
        new_command = []
        for c in cur_command:
            new_command.append(c)
        new_command.append(char)
        new_command = ''.join(new_command)
        return new_command

    @classmethod
    def validate_command(cls, command: str) -> bool:
        """Validates the commands. Return if command is valid."""
        numeric = int(''.join(re.findall(r'\d+', command))) if (re.search(r'\d', command)) else 1
        alphabetical = ''.join(re.findall(r'[a-zA-Z]+', command))

        match alphabetical:
            case "i":
                Application.switch_mode("insert")

            case "W":
                return cls.move_cursor("up", Application.selected_tab_frame.textbox, numeric)
            case "S":
                return cls.move_cursor("down", Application.selected_tab_frame.textbox, numeric)
            case "D":
                return cls.move_cursor("right", Application.selected_tab_frame.textbox, numeric)
            case "A":
                return cls.move_cursor("left", Application.selected_tab_frame.textbox, numeric)
            case "F":
                return cls.move_cursor("up", Application.selected_tab_frame.textbox, "0")
            case "V":
                return cls.move_cursor("down", Application.selected_tab_frame.textbox, "end")
            case "dd":
                return cls.delete_line_content(del_range=numeric)
            case "sq" | "wq":
                cls.save_file()
                exit(0)

            case "ww":
                return cls.save_file()

            case "qq":
                exit(0)

        return False

    @classmethod
    def delete_line_content(cls, del_range: int):
        t = Application.selected_tab_frame.textbox
        current_line = t.index("insert").split('.')[0]

        t.configure(state="normal")
        
        start = f"{current_line}.0"
        end = f"{int(current_line) + del_range}.0" if del_range != 0 else (float(start) + 1)

        t.delete(start, end)
        t.configure(state="disabled")
        return True
    
    @classmethod
    def move_cursor(cls, to: str, t: tk.Text, mov_range: int | str):
        cur_line   = int(t.index("insert").split('.')[0])
        cur_column = int(t.index("insert").split('.')[1])
        new_cursor_pos = f"{cur_line}.{cur_column}"

        match to:
            case "up":
                y = mov_range if isinstance(mov_range, str) else cur_line - mov_range
                new_cursor_pos = f"{y}.{cur_column}"
            case "down":
                y = mov_range if isinstance(mov_range, str) else cur_line + mov_range
                new_cursor_pos = "end" if mov_range == "end" else f"{y}.{cur_column}"
            case "left":
                new_cursor_pos = f"{cur_line}.{cur_column - mov_range}"
            case "right":
                new_cursor_pos = f"{cur_line}.{cur_column + mov_range}"

        t.mark_set("insert", new_cursor_pos)
        t.see(new_cursor_pos)
        return True

    @classmethod
    def save_file(cls):
        cur_file_path = Application.mainapp.file_name
        if not cur_file_path:
            cur_file_path = os.path.join(Application.mainapp.terminal_dir, "untitled.txt")

        content = Application.selected_tab_frame.textbox.get("1.0", "end-1c")
        with open(cur_file_path, "w", encoding="utf8") as f:
            f.write(content)
        return True
