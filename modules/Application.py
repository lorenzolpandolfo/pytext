from dataclasses import dataclass, field


@dataclass
class Application:
    mainapp: None
    selected_tab_frame: None
    current_file_path: str = ""
    mode: str = "view"
    all_open_files = {}

    @classmethod
    def set_mode(cls, arg: str):
        cls.mode = arg
    
    @classmethod
    def get_mode(cls):
        return cls.mode
    
    @classmethod
    def switch_mode(cls, forced_set: str = ''):
        cls.mode = forced_set if forced_set else "view" if cls.mode == "insert" else "insert"
        cls.mainapp.bottom_frame.mode.configure(text=cls.mode)
        state = "disabled" if cls.mode == "view" else "normal"
        widget = cls.mainapp.nametowidget(cls.selected_tab_frame)
        cls.mainapp.bottom_frame.command.configure(text="")
        # checar se isso é ok:
        if not widget.textbox:
            return
        widget.textbox.configure(state=state)

    @classmethod
    def set_current_file(cls, path):
        cls.mainapp.file_name = path
        cls.current_file_path = path
        cls.mainapp.bottom_frame.output.configure(text=path)

    @classmethod
    def remove_frame(cls, file_path: str = ""):
        if not file_path:
            file_path = Application.current_file_path
        for frame_id, data in Application.all_open_files.items():
            if str(data["file_path"]) == str(file_path):
                cls.mainapp.top_frame.notebook.forget(data["frame"])
                del Application.all_open_files[frame_id]
                return
