from modules.FileManager import FileManager as fm

class ThemeManager:
    @staticmethod
    def get_user_theme() -> str:
        try:
            fm.move_to_directory("user")
            return fm.open_json_file("theme.json")

        except Exception as error:
            print(f"Error: could not load 'user/theme.json'. Loading f_theme.json instead.")
            fm.move_to_directory("user", "fallbacks")
            return fm.open_json_file("f_theme.json")
