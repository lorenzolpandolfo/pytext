import os.path
import subprocess
import platform
from modules.LanguageManager import LanguageManager

from modules.Application import Application


class ScriptRunner:

    @staticmethod
    def run_script(e=None):
        path = Application.mainapp.file_title
        if not os.path.isfile(path):
            return False

        file_directory = os.path.dirname(path)

        command = LanguageManager.get_info("run").replace("CURRENT_FILE", path)
        if not ScriptRunner.is_command_safe(command):
            print(f"The command below is harmless to the system and was blocked.\ncommand: {command}")
            return False

        ScriptRunner.run_command_by_system(command, file_directory)

    @staticmethod
    def is_command_safe(cmd: str):
        blacklist = ["rm -rf", "del", "mkfs", "diskpart", "sudo", "sudo rm rf /", "regedit", "curl | bash", "netsh"]
        for blocked_prompt in blacklist:
            if blocked_prompt in cmd:
                return False
        return True

    @staticmethod
    def run_command_by_system(cmd: str, file_directory: str):
        system = platform.system()

        if system == "Linux":
            ScriptRunner.run_linux(cmd, file_directory)
        elif system == "Windows":
            ScriptRunner.run_windows(cmd, file_directory)

    @staticmethod
    def run_linux(cmd: str, file_directory: str):
        # X display server case
        if os.environ.get("DISPLAY") is not None:
            final_cmd = f'cd {file_directory}; bash -c "{cmd}; read -n 1"'
            subprocess.run(['x-terminal-emulator', '-e', final_cmd])

        # Wayland server case
        elif os.environ.get("WAYLAND_DISPLAY") is not None:
            print("using Wayland! This feature is not done yet. Use X instead.")

        else:
            print(f"[x] An error ocurried trying to run this file:\n{cmd}\nPlease, open an issue in Github.")

    @staticmethod
    def run_windows(cmd: str, file_directory: str):
        final_cmd = f'cmd /c "{cmd} & set /p dummy= "'
        try:
            subprocess.Popen(final_cmd, cwd=file_directory, creationflags=subprocess.CREATE_NEW_CONSOLE)
        except subprocess.CalledProcessError:
            return
