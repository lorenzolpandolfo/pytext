from dataclasses import dataclass
from modules.Application import Application
import re

@dataclass
class CommandManager:
    mainapp:str
    Application:Application

    @classmethod
    def validate_command(cls, command:str, *args):
        print("Command manager recieved: ", command)

        numeric = int(''.join(re.findall(r'\d+', command))) if (re.search(r'\d', command)) else 1
        alphabetical = ''.join(re.findall(r'[a-zA-Z]+', command))

        match alphabetical:
            case "i":
                Application.switch_mode()

            case "w":
                return cls.move_cursor("up", cls.mainapp.main_frame.textbox, numeric)
            case "s":
                return cls.move_cursor("down", cls.mainapp.main_frame.textbox, numeric)
            case "D":
                return cls.move_cursor("right", cls.mainapp.main_frame.textbox, numeric)
            case "a":
                return cls.move_cursor("left", cls.mainapp.main_frame.textbox, numeric)

            case "dd":
                return cls.delete_line_content(range=numeric)
            case "sq" | "wq":
                print("sair e salvar")
        return False
            
    
    @classmethod
    def delete_line_content(cls, range:int):
        textbox = cls.mainapp.main_frame.textbox 
        current_line = textbox.index("insert").split('.')[0]

        textbox.configure(state="normal")
        
        start = f"{current_line}.0"
        end = f"{int(current_line) + range}.0" if range != 0 else (float(start) + 1)

        textbox.delete(start, end)
        textbox.configure(state="disabled")
        return True
    
    @classmethod
    def move_cursor(cls, to:str, textbox, range:int):
        cur_line   = int(textbox.index("insert").split('.')[0])
        cur_column = int(textbox.index("insert").split('.')[1])

        match to:
            case "up":
                new_cursor_pos = f"{cur_line - range}.{cur_column}"
            case "down":
                new_cursor_pos = f"{cur_line + range}.{cur_column}"
            case "left":
                new_cursor_pos = f"{cur_line}.{cur_column - range}"
            case "right":
                new_cursor_pos = f"{cur_line}.{cur_column + range}"


        textbox.mark_set("insert", new_cursor_pos)
        textbox.see(new_cursor_pos)
        return True

    # @classmethod
    # def switch_mode(cls):
    #     cls.mode = "view" if cls.mode == "insert" else "insert"
    #     cls.mainapp.bottom_frame.mode.configure(text=cls.mode)
    #     state = "disabled" if cls.mode == "view" else "normal"
    #     cls.mainapp.main_frame.textbox.configure(state=state)
    #     cls.mainapp.bottom_frame.command.configure(text="")


    # def switch_mode(self):
    #     self.mode = "view" if self.mode == "insert" else "insert"
    #     self.bottom_frame.mode.configure(text=self.mode)

    #     Application.set_mode(self.mode)

    #     state = "disabled" if self.mode == "view" else "normal"
    #     self.main_frame.textbox.configure(state=state)

    #     self.bottom_frame.command.configure(text="")