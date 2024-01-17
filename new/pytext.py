import customtkinter as ctk

class MainApp(ctk.CTk):
	def __init__(self):
		super().__init__()

		self.__create_window__()
		self.__configure_grids__()
		self.__create_frames__()

		max_lines = self.main_frame.get_number_of_visible_lines()
		self.left_frame.create_counter(max_lines=max_lines)
		self.main_frame.set_textbox_height(height=max_lines)
	

	def __create_window__(self):
		self.title("The Pytext Editor Refactored")
		self.geometry("1100x749")
		self.resizable(True, True)

	def __configure_grids__(self):
		self.grid_rowconfigure(0, weight=1)
		self.grid_rowconfigure(1, weight=0)

		self.grid_columnconfigure(0, weight=0, minsize=60)
		self.grid_columnconfigure(1, weight=1)

	def __create_frames__(self):
		self.bottom_frame = BottomFrame(self)
		self.bottom_frame.grid(row=1, column=0, sticky="we", columnspan=2, rowspan=2)

		self.main_frame = MainFrame(self)
		self.main_frame.grid(row=0, column=1, sticky="nsew")

		self.left_frame = LeftFrame(self)
		self.left_frame.grid(row=0, column=0, sticky="ns")


class LeftFrame(ctk.CTkFrame):
	def __init__(self, master):
		super().__init__(master)

		
	def create_counter(self, max_lines:int):
		for i in range(0,max_lines):
			pady = (9,0) if i == 0 else (0,0)
			self.i = ctk.CTkLabel(self, text=i, anchor="e", font=ctk.CTkFont("Consolas", 30))
			self.i.grid(row=i, column=0, pady=pady)
	

	

class BottomFrame(ctk.CTkFrame):
	def __init__(self, master):
		super().__init__(master)

		self.mode = ctk.CTkLabel(self, text="Insert")
		self.mode.grid(row=1, column=0)

		self.output = ctk.CTkLabel(self, text="Welcome to Pytext refactored")
		self.output.grid(row=2, column=0)


class MainFrame(ctk.CTkFrame):
	def __init__(self, master):
		super().__init__(master)

		self.grid_rowconfigure(0, weight=1)
		self.grid_columnconfigure(0, weight=1)

		self.textbox = ctk.CTkTextbox(self, font=ctk.CTkFont("Consolas", 30))
		self.textbox.grid(row=0, column=0, sticky="new")

	
	def get_number_of_visible_lines(self):
		self.update()
		height = self.winfo_height()
		line_height = ctk.CTkFont("Consolas", 30).metrics()["linespace"]
		return height // line_height


	def set_textbox_height(self, height:int):
		return self.textbox._textbox.configure(height=height)


if __name__ == "__main__":
	app = MainApp()
	app.mainloop()
