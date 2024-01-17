import customtkinter as ctk

class MainApp(ctk.CTk):
	def __init__(self):
		super().__init__()

		self.grid_rowconfigure(0, weight=1)

		self.grid_columnconfigure(0, weight=1, uniform="columns", minsize=70)
		self.grid_columnconfigure(1, weight=20, uniform="columns")

		self.title("The Pytext Editor Refactored")
		self.geometry("1100x749")
		self.resizable(True, True)


		self.left_frame = LeftFrame(self)
		self.left_frame.grid(row=0, column=0, sticky="ns")

		self.main_frame = MainFrame(self)
		self.main_frame.grid(row=0, column=1, sticky="nsew")

		self.bottom_frame = BottomFrame(self)
		self.bottom_frame.grid(row=1, column=0, sticky="we", columnspan=2, rowspan=2)


class LeftFrame(ctk.CTkFrame):
	def __init__(self, master):
		super().__init__(master)
	
		for i in range(0,10):
			__pady = 10 # if i == 0 else 0
			self.i = ctk.CTkLabel(self, text=i, pady=(f"{__pady}.0"), font=ctk.CTkFont("Consolas", 30))
			self.i.grid(row=i, column=0)

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
		self.textbox.grid(row=0, column=0, sticky="nsew")


if __name__ == "__main__":
	app = MainApp()
	app.mainloop()

