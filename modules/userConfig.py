import json

class UserConfig:
    def __init__(self, root):
        self.root = root
    
    def load_user_config(self):
        with open("config.json", "r") as file:
            self.userconfig = json.load(file)
        
        self.selected_line_background_color = self.userconfig["line_background_color"]
        self.programming_language_format = self.userconfig["programming_language_format"]
        self.auto_insert_delimiters = self.userconfig["auto_insert_delimiters"]

        print(self.userconfig)