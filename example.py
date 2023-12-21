import tkinter as tk

class App:
    def __init__(self, root):
        self.root = root
        self.root.geometry("300x200")
        self.root.bind("<Key>", self.on_resize)

        self.textbox = tk.Text(root, wrap="word")
        self.textbox.grid(row=0, column=0, sticky="new")
        
        
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

    def on_resize(self, event):
        
        print(event.height)
        print(self.root.winfo_height() // 19)
        self.textbox.config(height=(self.root.winfo_height() // 19))
        

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
