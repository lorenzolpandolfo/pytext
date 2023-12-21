import json
import customtkinter as ctk

class UserConfig:
    def __init__(self, root):
        self.root = root
    
    def load_user_config(self):
        with open("config.json", "r") as file:
            self.config = json.load(file)
        
        self.selected_line_background_color = self.config["line_background_color"]
        self.programming_language_format = self.config["programming_language_format"]
        self.auto_insert_delimiters = self.config["auto_insert_delimiters"]

        print(self.config)
    

    def check_delimiter_chars(self, event, maintext):
        if self.config["auto_insert_delimiters"]:
                char_pressed = event.char
                if char_pressed in ["[", "(", "{", '"', "'"]:

                    dc = {
                        "[": "]",
                        "{": "}",
                        "(": ")",
                        '"': '"',
                        "'": "'"
                    }
                    
                    linha_atual = int(maintext.index(ctk.INSERT).split(".")[0])
                    coluna_atual = int(maintext.index(ctk.INSERT).split(".")[1])

                    maintext.insert(ctk.INSERT, dc[char_pressed])
                    maintext.mark_set(ctk.INSERT, f"{linha_atual}.{coluna_atual}")
                    return 0
            