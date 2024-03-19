from dataclasses import dataclass
from modules.Application import Application

@dataclass
class CommandManager:
    mainapp:str
    Application:Application

    @classmethod
    def validate_command(cls, command:str, *args):
        print("Command manager recieved: ", command)
        match command:
            case "i":
                Application.switch_mode()
            case "dd":
                print("deletando")
            case "sq" | "wq":
                print("sair e salvar")
    
    # @classmethod
    # def switch_mode(cls):
    #     cls.mode = "view" if cls.mode == "insert" else "insert"
    #     cls.mainapp.bottom_frame.mode.configure(text=cls.mode)
    #     state = "disabled" if cls.mode == "view" else "normal"
    #     cls.mainapp.main_frame.textbox.configure(state=state)
    #     cls.mainapp.bottom_frame.command.configure(text="")


    # def switch_mode(self):
    #     self.mode = "view" if self.mode == "insert" else "insert"
    #     self.bottom_frame.mode.configure(text=self.mode)

    #     Application.set_mode(self.mode)

    #     state = "disabled" if self.mode == "view" else "normal"
    #     self.main_frame.textbox.configure(state=state)

    #     self.bottom_frame.command.configure(text="")