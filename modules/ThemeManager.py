import json
import os

class ThemeManager:
    @staticmethod
    def get_user_theme() -> str:
        ThemeManager.__move_to_user_directory__()
        return ThemeManager.__load_theme_file__()


    @staticmethod
    def __move_to_user_directory__():
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        os.chdir("..")
        os.chdir("user")
    

    @staticmethod
    def __load_theme_file__():
        with open("theme.json", "r", encoding="utf8") as file:
            return json.load(file)
