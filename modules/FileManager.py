import os

class FileManager:
    """Deals with file management. Used to open files and directories, check if path is a file or directory, etc."""

    @staticmethod
    def open_file(file_path:str) -> str | bool:
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
    def open_directory(dir_path:str) -> list | bool:
        """Returns a list with all files and directories inside the directory argument."""
        pass

    @staticmethod
    def check_if_file_or_dir(path:str) -> str | bool:
        """Checks if a path is a file or a directory."""
        if not os.path.exists(path):
            return False
        
        elif os.path.isfile():
            return "file"
        
        elif os.path.isdir():
            return "dir"
