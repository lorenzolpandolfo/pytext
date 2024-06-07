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

            case "W":
                return cls.move_cursor("up", cls.mainapp.main_frame.textbox, numeric)
            case "S":
                return cls.move_cursor("down", cls.mainapp.main_frame.textbox, numeric)
            case "D":
                return cls.move_cursor("right", cls.mainapp.main_frame.textbox, numeric)
            case "A":
                return cls.move_cursor("left", cls.mainapp.main_frame.textbox, numeric)

            case "dd":
                return cls.delete_line_content(range=numeric)

            case "sq" | "wq":
                print("sair e salvar")
                return cls.save_file()

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
    def move_cursor(cls, to: str, textbox, range: int):
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

    @classmethod
    def save_file(cls):
        cur_file_path = Application.mainapp.file_name
        if not cur_file_path:
            return False

        content = Application.mainapp.main_frame.textbox.get("1.0", "end-1c")
        with open(cur_file_path, "w", encoding="utf8") as f:
            r = f.write(content)
        print(r)
        return r

        #def save(textbox, mainapp, gui):
#
        #    if mainapp.FileManager.file_name != "":
        #        # print("FILE NAME: ", mainapp.FileManager.file_name)
        #        # In this case, you're saving the SavePreset file
        #        if mainapp.FileManager.file_name == "__pytextSavePreset__":
        #            mainapp.FileManager.file_name = textbox.get("1.0", "1.end")
        #            content = gui.buffer_content
#
        #        # Creating a new dir title
        #        elif mainapp.FileManager.file_name == "__pytextNewDirTitle__":
        #            dir_name = textbox.get("1.0", "1.end")
        #            return mainapp.FileManager.create_new_directory(dir_name, textbox, mainapp)
#
        #        else:
        #            # Get all the content in this current file
        #            content = textbox.get("1.0", "end-1c")
        #            gui.buffer_content = content
#
        #        full_path = os.path.join(mainapp.FileManager.terminal_directory, mainapp.FileManager.file_name)
#
        #        with open(full_path, "w", encoding="utf8") as new_file:
        #            new_file.write(content)
#
        #            # check if you just added a title to a non-title file
        #            if mainapp.FileManager.file_name == textbox.get("1.0", "1.end"):
        #                # Loading the old file
        #                gui.write_another_file_content(gui.buffer_content, file_name=textbox.get("1.0", "1.end"))
#
        #            return f"{mainapp.FileManager.file_name} saved"
#
        #    # this runs when you save a file that doesn't have a title yet
        #    else:
        #        # Saving the current file content so you can edit the SavePreset file
        #        gui.buffer_content = textbox.get("1.0", ctk.END)
#
        #        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        #        os.chdir("..")
        #        savepreset = os.path.join(os.getcwd(), ".temp", "__pytextSavePreset__.txt")
#
        #        with open(savepreset, "r", encoding="utf8") as savepresetfile:
        #            content = savepresetfile.read()
        #            gui.write_another_file_content(content, "", True)
#
        #        mainapp.FileManager.file_name = "__pytextSavePreset__"
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