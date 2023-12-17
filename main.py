import tkinter as tk
from tkinter import font
import customtkinter as ctk


class MainApp:
    def __init__(self, root):
        self.root = root
        self.modo = "view"
        self.create_window()
        self.create_frames()
        self.create_widgets()
        self.capture_commands()
        self.combo = []



    def create_window(self):
        root.geometry("1100x780")
        self.root.title("The Pytext Editor")
    

    def create_frames(self):
        # creating left frame
        self.leftframe = ctk.CTkFrame(root)
        self.leftframe.grid(row=0, column=0, sticky="ns")
        # peso 0 para não expandir (janela)
        self.root.columnconfigure(0, weight=0)

        # creating the main frame
        self.mainframe = ctk.CTkFrame(root)
        self.mainframe.grid(row=0, column=1, sticky="nsew")
        # peso 1 para que ele expanda (janela)
        self.root.columnconfigure(1, weight=1)
        self.root.rowconfigure(0, weight=1)

        # creating bottom frame
        self.bottomframe = ctk.CTkFrame(root)
        self.bottomframe.grid(row=1, column=0, columnspan=2, sticky="ew")


    def create_widgets(self):
        # initializing firacode font
        src = r"fonts\firacode.ttf"
        # carrega a fonte
        ctk.FontManager.load_font(src)
        # agora ele reconhece a family Fira Code, porque eu carreguei antes
        firacode = ctk.CTkFont(family="Fira Code", size=19) 

        # initializing main text area
        self.main_textarea = ctk.CTkTextbox(self.mainframe, wrap=ctk.WORD, font=firacode)
        self.main_textarea.grid(row=0, column=0, sticky="nsew", padx=10, pady=(20, 10))
        self.main_textarea.focus_set()
        self.main_textarea.configure(state="disabled")


        # configurando o mainframe
        self.mainframe.columnconfigure(0, weight=1)
        self.mainframe.rowconfigure(0, weight=1)

        # initializing left text area
        self.left_textarea = ctk.CTkTextbox(self.leftframe, width=50, wrap=ctk.CHAR, font=firacode)
        self.left_textarea.grid(row=0, column=0, sticky="ns", padx=(10,10), pady=(20,10))
        # configurando o leftframe
        self.leftframe.columnconfigure(0, weight=1)
        self.leftframe.rowconfigure(0, weight=1)

        # creating the bottom label
        self.bottom_output_mode = ctk.CTkLabel(self.bottomframe, text=self.modo, justify="center", font=firacode)
        self.bottom_output_mode.grid(row=1, column=0, sticky="ew", columnspan=2)

        # Criando o textbox no segundo grid
        self.bottom_command_output = ctk.CTkTextbox(self.bottomframe, font=firacode, width=100, height=2)
        # Como o sticky é "e", ele vai ser ancorado para o leste ->
        self.bottom_command_output.grid(row=1, column=1, sticky="e", padx=(0, 10), pady=(0, 5))

        # o peso é 1 para que ele se mova para a direita
        self.bottomframe.columnconfigure(1, weight=1)
        # Configurando o textbox para ser menor verticalmente
        self.bottom_command_output.rowconfigure(1, weight=0)  # Ajuste para tornar a segunda linha menor


    def capture_commands(self):
        # ele envia argumentos mesmo sem indicar
        root.bind("<Key>", self.tecla_pressionada)
        root.bind("<Button-1>", self.atualizar_contador)
        root.bind("<Escape>", lambda e: self.trocar_modo(self.modo))
    

    def trocar_modo(self, modo):
        if modo == "view":
            # caso vc aperte ESC com comando definido na caixa, ele so apaga o comando. Nao troca de modo
            if self.bottom_command_output.get("1.0", "end-1c") != "":
                self.bottom_command_output.delete("1.0", ctk.END)
                self.main_textarea.focus_set()
                return 0

            self.modo = "insert"
            self.main_textarea.configure(state="normal")
            self.main_textarea.focus_set()
        else:
            self.modo = "view"
            self.main_textarea.configure(state="disabled")
        
        self.bottom_command_output.delete("1.0", ctk.END)
        print(self.modo)
        return self.bottom_output_mode.configure(text=self.modo)


    def tecla_pressionada(self, event):
        tecla = event.keysym
        print(event)

        if tecla == "colon":
            print(": pressionado")
            # caso esteja no modo view, e vc aperta um tecla, ele adiciona a tecla na caixa de comandos e dá o foco nela
            if self.modo == "view":
                if self.bottom_command_output.get("1.0", "end-1c") == "":
                    self.bottom_command_output.focus_set()

                print("Registrando comandos")
        
        
        if self.modo == "view":
            match tecla:
                case "i":
                    return self.trocar_modo(self.modo)

                case _:
                    return 0
                
        
        match tecla:
            case "Up"| "Down"| "Left"| "Right"| "Return" |"BackSpace" |"Button-1":
                print("necessita atualizar contador! - ", tecla)
                return self.atualizar_contador()
            case _:
                return 0


    def atualizar_contador(self, event = None):
        print("contador atualizado!", event)
        return 0

if __name__ == "__main__":
    root = ctk.CTk()
    app = MainApp(root)
    root.mainloop()