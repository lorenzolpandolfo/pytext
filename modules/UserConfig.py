from modules.FileManager import FileManager as fm

class UserConfig:
    @staticmethod
    def get_user_config():
        try:
            fm.move_to_directory("user")
            return fm.open_json_file("config.json")
        
        except Exception as error:
            print(f"Error: could not load 'user/config.json'. Loading f_config.json instead.")
            fm.move_to_directory("user", "fallbacks")
            return fm.open_json_file("f_config.json")
