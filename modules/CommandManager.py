import os
import tkinter
from dataclasses import dataclass
from modules.Application import Application
from modules.FileManager import FileManager as fm
import re


@dataclass
class CommandManager:
    mainapp: str
    Application: Application

    @classmethod
    def validate_command(cls, command: str, *args):
        # print("Command manager recieved: ", command)

        numeric = int(''.join(re.findall(r'\d+', command))) if (re.search(r'\d', command)) else 1
        alphabetical = ''.join(re.findall(r'[a-zA-Z]+', command))

        match alphabetical:
            case "i":
                Application.switch_mode()

            case "W":
                return cls.move_cursor("up", cls.mainapp.main_frame.textbox, numeric)
            case "S":
                return cls.move_cursor("down", cls.mainapp.main_frame.textbox, numeric)
            case "D":
                return cls.move_cursor("right", cls.mainapp.main_frame.textbox, numeric)
            case "A":
                return cls.move_cursor("left", cls.mainapp.main_frame.textbox, numeric)
            case "F":
                return cls.move_cursor("up", cls.mainapp.main_frame.textbox, "0")
            case "V":
                return cls.move_cursor("down", cls.mainapp.main_frame.textbox, "end")
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
        textbox = cls.mainapp.main_frame.textbox 
        current_line = textbox.index("insert").split('.')[0]

        textbox.configure(state="normal")
        
        start = f"{current_line}.0"
        end = f"{int(current_line) + del_range}.0" if del_range != 0 else (float(start) + 1)

        textbox.delete(start, end)
        textbox.configure(state="disabled")
        return True
    
    @classmethod
    def move_cursor(cls, to: str, textbox, mov_range: int | str):
        cur_line   = int(textbox.index("insert").split('.')[0])
        cur_column = int(textbox.index("insert").split('.')[1])
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

        textbox.mark_set("insert", new_cursor_pos)
        textbox.see(new_cursor_pos)
        return True

    @classmethod
    def save_file(cls):
        cur_file_path = Application.mainapp.file_name
        if not cur_file_path:
            cur_file_path = os.path.join(Application.mainapp.terminal_dir, "untitled.txt")

        content = Application.mainapp.main_frame.textbox.get("1.0", "end-1c")
        with open(cur_file_path, "w", encoding="utf8") as f:
            f.write(content)
        return True

    @classmethod
    def comment_lines(cls, textbox):
        if Application.mode != "insert":
            return False

        fm.move_to_directory("languages")
        comments = fm.open_json_file("comments.json")
        cur_file = Application.mainapp.file_name
        _, file_ext = os.path.splitext(cur_file)
        comment_symbol = comments[file_ext]

        selected_lines = CommandManager.get_selected_lines(textbox)
        if not selected_lines:
            selected_lines = [textbox.index("insert").split('.')[0]]

        for line in selected_lines:
            start_index = f"{line}.0"
            current_line_text = textbox.get(start_index, f"{line}.end")

            if current_line_text.startswith(comment_symbol):
                textbox.delete(start_index, f"{line}.{len(comment_symbol) + 1}")
            else:
                textbox.insert(start_index, f"{comment_symbol} ")
        return True

    @classmethod
    def get_selected_lines(cls, textbox):
        try:
            start = textbox.index("sel.first")
            end = textbox.index("sel.last")
            start_line = int(start.split('.')[0])
            end_line = int(end.split('.')[0])
            selected_lines = list(range(start_line, end_line + 1))
            return selected_lines
        except tkinter.TclError:
            return []
