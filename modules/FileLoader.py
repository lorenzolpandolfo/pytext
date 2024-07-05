import os

from modules.Application import Application
from modules.LanguageManager import LanguageManager
from modules.FileManager import FileManager


class FileLoader:

    @staticmethod
    def open_file(file_path: str) -> str | bool:
        """Returns file content to be loaded."""
        if os.path.isfile(file_path):
            try:
                with open(file_path, "r", encoding="utf8") as file:
                    content = file.read()
                    Application.current_file_path = file_path
                    title = os.path.basename(file_path)
                    Application.mainapp.main_frame.add_tab(title, content, file_path)

                    _, file_ext = os.path.splitext(file_path)
                    LanguageManager.load_language(file_ext)
                    Application.set_current_file(file_path)

            except UnicodeDecodeError:
                print(f"[X] Unicode decode error with file {file_path}")
                return False
        else:
            title = os.path.basename(file_path)
            Application.mainapp.main_frame.add_tab(tab_title=title, content='', file_path=file_path)
            _, file_ext = os.path.splitext(file_path)
            LanguageManager.load_language(file_ext)
            Application.set_current_file(file_path)

    @classmethod
    def open_welcome_file(cls):
        FileManager.move_to_directory()
        file = os.path.join(os.getcwd(), "welcome")
        cls.open_file(file)
        Application.current_file_directory = ""

    @classmethod
    def open_config_file(cls):
        FileManager.move_to_directory("user")
        file = os.path.join(os.getcwd(), "config.json")
        cls.open_file(file)
