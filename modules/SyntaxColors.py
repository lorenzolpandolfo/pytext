import os
import json

class SyntaxColors:
    
    @staticmethod
    def get_syntax_colors():
        SyntaxColors.__move_to_user_directory__()
        return SyntaxColors.__load_config_file__()


    @staticmethod
    def __load_config_file__():
        with open("syntaxColors.json", "r", encoding="utf8") as file:
            return json.load(file)


    @staticmethod
    def __move_to_user_directory__():
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        os.chdir("..")
        os.chdir("user")