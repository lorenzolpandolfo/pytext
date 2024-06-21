from dataclasses import dataclass

from modules.FileManager import FileManager as Fm


@dataclass
class LanguageManager:
    language_data = None
    file_extension   = None

    @staticmethod
    def load_language(language):
        if not language:
            return False
        Fm.move_to_directory("languages")

        content = Fm.open_json_file(language)
        if not content:
            return False

        LanguageManager.language_data = content
        LanguageManager.file_extension  = language
        return content

    @staticmethod
    def get_info(info):
        try:
            return LanguageManager.language_data[info]
        except Exception:
            return ''