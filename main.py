import tkinter as tk
import customtkinter as ctk
import re
import random

import shortcuts



class MainApp:
    def __init__(self, root):
        self.root = root
        self.modo = "view"

        # inicializando as classes
        
        self.gui = GUI(self.root)
        self.command_manager = CommandManager(self.root)

        self.gui.main_app_instance = self
        self.command_manager.main_app_instance = self
        
        self.gui.start()

        self.gui.setup(self, self.command_manager)
        self.command_manager.setup(self, self.gui.main_textarea, self.gui.bottom_command_output, self.gui)

        self.command_manager.capture_commands()        
        self.combo = []



class CommandManager:
    def __init__(self, root:ctk.CTk()):
        self.root = root

    def setup(self, main_app_instance:MainApp, main_textarea:ctk.CTkTextbox, bottom_command_output:ctk.CTkTextbox,
              gui_instance):
        self.maintext = main_textarea
        self.bottom_command_output = bottom_command_output
        self.main_app_instance = main_app_instance
        self.gui = gui_instance


    def capture_commands(self):
        # ele envia argumentos mesmo sem indicar
        self.root.bind("<Key>", self.tecla_pressionada)
        self.root.bind("<Escape>", lambda e: self.trocar_modo(self.main_app_instance.modo))
        # Atualizar as labels para ajustar na resolução
        self.root.bind("<Prior>", lambda e: self.gui.criar_contador(e))
        self.maintext.bind("<MouseWheel>", lambda e: "break")

    
    def trocar_modo(self, modo):
        if modo == "view":
            # caso vc aperte ESC com comando definido na caixa, ele so apaga o comando. Nao troca de modo
            comando = self.bottom_command_output.get("1.0", "end-1c")

            if comando != "":
                self.bottom_command_output.delete("1.0", ctk.END)
                self.maintext.focus_set()
                return 0

            self.main_app_instance.modo = "insert"
            self.maintext.configure(state="normal")
            self.maintext.focus_set()
            self.gui.bottom_output_detail.configure(text="")
        else:
            self.main_app_instance.modo = "view"
            self.maintext.configure(state="disabled")
        
        self.bottom_command_output.delete("1.0", ctk.END)
        print(self.main_app_instance.modo)
        return self.gui.bottom_output_mode.configure(text=self.main_app_instance.modo)


    def tecla_pressionada(self, event):
        self.gui.realcar_linha_selecionada(self.gui)
        tecla = event.keysym
        #print(event)

        if self.main_app_instance.modo == "view":
            comando = self.bottom_command_output.get("1.0", "end-1c")
            
            # Caso não haja comandos e aperte :
            if comando == "":
                if tecla == "colon":
                    self.bottom_command_output.focus_set()

                else:
                    match tecla:
                        case "i":
                            return self.trocar_modo(self.main_app_instance.modo)
                        
                        case "Up" | "Down" | "Left" | "Right" | "Return" | "BackSpace" | "Button-1":
                            return self.gui.atualizar_contador(tecla)
                        
                        case _:
                            return 0

            # Caso aperte Enter para registrar o comando
            elif tecla == "Return":
                self.catch_comando(comando)
                self.maintext.focus_set()
 

        elif self.main_app_instance.modo == "insert":

            match tecla:
                case "Up" | "Down" | "Left" | "Right" | "Return" | "BackSpace" | "Button-1":
                    return self.gui.atualizar_contador(tecla)
                case _:
                    return 0


    def catch_comando(self, comando):
        # separando o comando em partes: numero de vezes a rodar e o comando
        def extrair_numeros(texto):
            numeros = re.findall(r'\d+', texto)
            if numeros:
                return int(''.join(numeros))
            else:
                return 0

        comando_sem_numeros = re.sub(r'\d', '', comando)
        numeros = extrair_numeros(comando)

        # tratando o comando de fato
        self.gui.bottom_output_detail.configure(text=shortcuts.search_command(comando_sem_numeros, numeros, self.maintext))
        self.gui.atualizar_contador()
        self.gui.realcar_linha_selecionada()

        
        # apagando o comando enviado
        self.bottom_command_output.delete("1.0", ctk.END)
        return 0



class GUI:
    def __init__(self, root):
        self.root = root
        self.labels = []
    

    def setup(self, main_app_instance:MainApp, command_manager_instance:CommandManager):
        self.main_app_instance = main_app_instance
        self.command_manager_instance = command_manager_instance

    def criar_contador(self, e = None):
        # Sem o update ele nao consegue calcular o num de linhas
        self.root.update()

        self.max_linhas_visiveis = self.calcular_numero_de_linhas_visiveis()
        self.criar_labels()




    def calcular_tamanho_caixa_de_texto(self):
        # precisa deste update para ele registrar o valor correto da resolução
        self.root.update()
        altura_janela = self.root.winfo_height()
        print(altura_janela)
        tam = self.root.winfo_height()
        # estranho isso, mas ta funcionando
        tam = tam/1.4
        print("Tamanho no frame: ", self.mainframe.winfo_height(), "Tam: ", tam)

        self.main_textarea.configure(height=(tam))
        print("Tamanho do texto alterado")




    def criar_labels(self):
        self.main_textarea.update_idletasks()
        num = self.calcular_numero_de_linhas_visiveis()

        for label in self.labels:
            label.destroy()

        # resetando o array
        self.labels = []

        self.main_textarea.update_idletasks()

        for i in range(0, num):
            if i == 0:
                label = ctk.CTkLabel(self.leftframe, text=str(i), font=self.firacode)
                label.grid(row=i, column=0, sticky="en", pady=(28.75,0))
            else:
                label = ctk.CTkLabel(self.leftframe, text=str(i), font=self.firacode)
                label.grid(row=i, column=0, sticky="en", pady=(0))

            #label.rowconfigure(i,weight=1)
            self.labels.append(label)
        

    def realcar_linha_selecionada(self, objeto = None):
        texto = self.main_textarea
        linha_atual = int(texto.index(tk.INSERT).split(".")[0])
        inicio_linha = f"{linha_atual}.0"
        fim_linha = f"{linha_atual + 1}.0"
        
        texto.tag_remove("realce", "1.0", tk.END)
        texto.tag_add("realce", inicio_linha, fim_linha)
        texto.tag_config("realce", background="#2b2b2b")


    def atualizar_contador(self, e=None):
        def add_zero_to_selected_line(self):
            # pegando o valor da linha selecionada dentre as visiveis
            self.label_value = self.get_visible_line(self.main_textarea)

            try:
                self.labels[self.label_value - 1].configure(text=999)
            except IndexError:
                print("linha cortada para tentar evitar dessincronização de contador")
                # 250 tira duas linhas, considerando tamanhos extras do widget
                self.main_textarea.configure(height=int(self.main_textarea.winfo_height()) - 200)

            # se o cursor se moveu
            try:
                if self.last_zero_pos != self.label_value - 1:
                    self.labels[self.last_zero_pos].configure(text=1)
                    
            except Exception:
                self.labels[self.label_value - 2].configure(text=1)
                
            
            # guardando a posicao antiga do cursor
            self.last_zero_pos = self.label_value - 1

            return calcular_distancias([int(label.cget("text")) for label in self.labels], self.label_value -1)


        def calcular_distancias(array, posicao_zero):
            # Calcular a distância entre cada elemento e o elemento 0
            distancias = [abs(i - posicao_zero) for i in range(len(array))]
            
            for i, valor in enumerate(distancias):
                if valor == 0:
                    distancias[i] = int(self.main_textarea.index(ctk.INSERT).split(".")[0])

            return distancias
        
        self.vals = add_zero_to_selected_line(self)


        # mostrando o contador
        for i, label in enumerate(self.labels):
            label.configure(text=self.vals[i])
        return 0
    

    def get_visible_line(self, text_widget):
        # Obtém a informação da linha atual
        cursor_pos = text_widget.index(tk.INSERT)
        line_number = int(cursor_pos.split('.')[0])
        
        # Calcula a primeira linha visível na tela
        first_visible_line = int(text_widget.index("@0,0").split('.')[0])
        
        # Calcula a linha visível atual
        visible_line = line_number - first_visible_line + 1
        
        return visible_line



    def calcular_numero_de_linhas_visiveis(self):
        self.main_textarea.update_idletasks()  # Atualiza a geometria antes de calcular
        self.main_textarea.update()
        self.calcular_tamanho_caixa_de_texto()

        try:
            height = self.main_textarea.winfo_height()
            line_height = self.main_textarea.dlineinfo("1.0")[3]  # Altura da primeira linha
            visible_lines = height // line_height
            print("num de linhas calculado")
            return visible_lines

        except TypeError:
            return self.max_linhas_visiveis


    def obter_numero_de_linhas_e_colunas(self):
        # Obtém o conteúdo do TextBox como uma string
        conteudo = self.main_textarea.get("1.0", "end-1c")
        linhas = conteudo.split('\n')
        
        numero_de_linhas = len(linhas)

        # maior valor de comprimento de linha por cada linha
        num_colunas = max(len(linha) for linha in linhas)

        return (numero_de_linhas, num_colunas)


    def start(self):
        self.create_window()
        self.create_frames()
        self.create_widgets()
        self.criar_contador()


    def create_window(self):
        root.geometry("1100x760")
        self.root.title("The Pytext Editor")


    def create_frames(self):
        # creating left frame
        self.leftframe = ctk.CTkFrame(root)
        self.leftframe.grid(row=0, column=0, sticky="ns", rowspan=10)
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
        self.firacode = ctk.CTkFont(family="Fira Code", size=19) 

        # initializing main text area
        # fazer com que ele tenha um tamanho sempre multiplo do tamanho das linhas
        self.main_textarea = ctk.CTkTextbox(self.mainframe, wrap=ctk.WORD, font=self.firacode)
        self.main_textarea.grid(row=0, column=0, sticky="new", padx=10, pady=(20, 10))
        self.main_textarea.focus_set()
        self.main_textarea.grid_rowconfigure(0, weight=1)

        


        self.main_textarea.configure(state="disabled", height=500)


        # escondendo a barra de scroll
        self.theme_mode = ctk.get_appearance_mode()
        self.themes = {
            "Dark": "#1d1e1e",
            "Light": "#f9f9fa"
        }
        self.main_textarea.configure(yscrollcommand="", scrollbar_button_color=self.themes[self.theme_mode], scrollbar_button_hover_color=self.themes[self.theme_mode])


        # configurando o mainframe
        self.mainframe.columnconfigure(0, weight=1)
        self.mainframe.rowconfigure(0, weight=1)

        # initializing left text area
        self.left_textarea = ctk.CTkTextbox(self.leftframe, width=70, wrap=ctk.CHAR, font=self.firacode)
        #self.left_textarea.grid(row=0, column=0, sticky="ns", padx=(10,10), pady=(20,10))

        # configurando o leftframe
        self.leftframe.columnconfigure(0, weight=0)
        self.leftframe.rowconfigure(0, weight=0)

        # creating the bottom label
        self.bottom_output_mode = ctk.CTkLabel(self.bottomframe, text=self.main_app_instance.modo, justify="center", font=self.firacode)
        self.bottom_output_mode.grid(row=1, column=0, sticky="ew", columnspan=2)

        self.bottom_output_detail = ctk.CTkLabel(self.bottomframe, text="", justify="left", font=self.firacode)
        self.bottom_output_detail.grid(row=1, column=1, sticky="e", padx=10)
        self.bottom_output_doc_info = ctk.CTkLabel(self.bottomframe, text="(10,56)", justify="left", font=self.firacode)
        self.bottom_output_doc_info.grid(row=1, column=0, sticky="e", padx=10)
        # Criando o textbox no segundo grid
        self.bottom_command_output = ctk.CTkTextbox(self.bottomframe, font=self.firacode, width=100, height=2)
        # Como o sticky é "e", ele vai ser ancorado para o leste ->
        self.bottom_command_output.grid(row=1, column=2, sticky="e", padx=(0, 10), pady=(0, 5))

        # o peso é 1 para que ele se mova para a direita
        self.bottomframe.columnconfigure(1, weight=1)
        # Configurando o textbox para ser menor verticalmente
        self.bottom_command_output.rowconfigure(1, weight=0)  # Ajuste para tornar a segunda linha menor



if __name__ == "__main__":
    root = ctk.CTk()
    app = MainApp(root)
    root.mainloop()