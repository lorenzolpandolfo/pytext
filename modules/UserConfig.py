from modules.FileManager import FileManager as Fm


class UserConfig:
    @staticmethod
    def get_user_config():
        try:
            Fm.move_to_directory("user")
            return Fm.open_json_file("config.json")
        
        except Exception:
            print(f"[ERROR] Could not load 'user/config.json'. Loading f_config.json instead.")
            Fm.move_to_directory("user", "fallbacks")
            return Fm.open_json_file("f_config.json")
