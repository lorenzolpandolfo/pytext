import os
import json


class FileManager:
    """Deals with file management. Used to open files and directories, check if path is a file or directory, etc."""

    @staticmethod
    def open_file(file_path: str) -> str | bool:
        """Returns file content to be loaded."""

        if os.path.isfile(file_path):
            try:
                with open(file_path, "r", encoding="utf8") as file:
                    return file.read()
            except UnicodeDecodeError:
                print(f"[X] Unicode decode error with file {file_path}")
                return False
        else:
            return False
        
    @staticmethod
    def open_directory(dir_path: str) -> tuple | bool:
        """Returns a tuple with raw and formatted strings of all files and directories inside the directory argument."""
        if os.path.isdir(dir_path):
            files = os.listdir(dir_path)
            raw_strfiles = "\n".join(files)

            formatted_strfiles = "\n".join(
                f" /{file}" if os.path.isdir(os.path.join(dir_path, file)) else f" {file}"
                for file in files
            )
            formatted_strfiles = f"▼ {os.path.split(dir_path)[-1]}\n" + formatted_strfiles

            return (raw_strfiles, formatted_strfiles)
        else:
            return False

    @staticmethod
    def check_if_repository(dir_path: str) -> bool:
        """Checks if a directory is a git repository."""
        full_path_directory = os.path.dirname(dir_path)

        if os.path.isdir(full_path_directory):
            return os.path.exists(os.path.join(full_path_directory, ".git"))
        return False
    
    @staticmethod
    def get_git_branch(git_path: str) -> str | bool:
        full_path_directory = os.path.dirname(git_path)
        full_path_directory = os.path.join(full_path_directory, ".git")

        if os.path.isdir(full_path_directory):
            os.chdir(full_path_directory)
            with open("HEAD", "r", encoding="utf8") as head_file:
                content = head_file.read()
                return content.split("/")[-1]
        return False

    @staticmethod
    def move_to_directory(*args):
        """Used to move inside a directory inside Pytext root directory."""
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        os.chdir("..")
        if args:
            for arg in args:
                os.chdir(arg)

    @staticmethod
    def open_json_file(file_title:str):
        with open(file_title, "r", encoding="utf8") as file:
            return json.load(file)
