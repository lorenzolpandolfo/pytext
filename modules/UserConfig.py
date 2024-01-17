import os
import json

class UserConfig:
    @staticmethod
    def get_user_config():
        UserConfig.__move_to_user_directory__()
        return UserConfig.__load_config_file__()
        

    @staticmethod
    def __move_to_user_directory__():
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        os.chdir("..")
        os.chdir("user")

    @staticmethod
    def __load_config_file__():
        with open("config.json", "r", encoding="utf8") as file:
            return json.load(file)

