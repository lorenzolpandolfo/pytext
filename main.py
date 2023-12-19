import tkinter as tk
from tkinter import font
import customtkinter as ctk
import re
import random

import shortcuts

class MainApp:
    def __init__(self, root):
        self.root = root
        self.modo = "view"
        self.create_window()
        self.create_frames()
        self.create_widgets()
        self.capture_commands()
        # Sem o update ele nao consegue calcular o num de linhas
        self.root.update()
        
        self.combo = []
        self.max_linhas_visiveis = self.calcular_numero_de_linhas_visiveis()
        self.num_to_labels = [str(x) for x in range(0,self.max_linhas_visiveis)]
        self.labels = []

        self.criar_labels()


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
        self.main_textarea = ctk.CTkTextbox(self.mainframe, wrap=ctk.WORD, font=self.firacode)
        self.main_textarea.grid(row=0, column=0, sticky="nsew", padx=10, pady=(20, 10))
        self.main_textarea.focus_set()
        self.main_textarea.configure(state="disabled")

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
        self.bottom_output_mode = ctk.CTkLabel(self.bottomframe, text=self.modo, justify="center", font=self.firacode)
        self.bottom_output_mode.grid(row=1, column=0, sticky="ew", columnspan=2)

        # Criando o textbox no segundo grid
        self.bottom_command_output = ctk.CTkTextbox(self.bottomframe, font=self.firacode, width=100, height=2)
        # Como o sticky é "e", ele vai ser ancorado para o leste ->
        self.bottom_command_output.grid(row=1, column=1, sticky="e", padx=(0, 10), pady=(0, 5))

        # o peso é 1 para que ele se mova para a direita
        self.bottomframe.columnconfigure(1, weight=1)
        # Configurando o textbox para ser menor verticalmente
        self.bottom_command_output.rowconfigure(1, weight=0)  # Ajuste para tornar a segunda linha menor


    def criar_labels(self):
        num = self.calcular_numero_de_linhas_visiveis()
        print(num)

            # Limpar labels existentes
        for label in self.labels:
            label.destroy()
        
        for i in range(0, num):
            if i == 0:
                label = ctk.CTkLabel(self.leftframe, text=str(i), font=self.firacode)
                label.grid(row=i, column=0, sticky="en", pady=(28.6,0))
            else:
                label = ctk.CTkLabel(self.leftframe, text=str(i), font=self.firacode)
                label.grid(row=i, column=0, sticky="en", pady=0)

            #label.rowconfigure(i,weight=1)
            self.labels.append(label)
        
        print(self.labels)

    def capture_commands(self):
        # ele envia argumentos mesmo sem indicar
        root.bind("<Key>", self.tecla_pressionada)
        root.bind("<Button-1>", self.atualizar_contador)
        root.bind("<Escape>", lambda e: self.trocar_modo(self.modo))
        self.main_textarea.bind("<MouseWheel>", lambda e: "break")

    

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
        #print(event)

        if self.modo == "view":
            comando = self.bottom_command_output.get("1.0", "end-1c")
            
            # Caso não haja comandos e aperte :
            if comando == "":
                if tecla == "colon":
                    self.bottom_command_output.focus_set()
                else:
                    match tecla:
                        case "i":
                            return self.trocar_modo(self.modo)
                        case "Up" | "Down" | "Left" | "Right" | "Return" | "BackSpace" | "Button-1":
                            return self.atualizar_contador(tecla)
                        case _:
                            return 0

                        

            # Caso aperte Enter para registrar o comando
            elif tecla == "Return":
                self.catch_comando(comando)
                self.main_textarea.focus_set()
 

        elif self.modo == "insert":

            match tecla:
                case "Up" | "Down" | "Left" | "Right" | "Return" | "BackSpace" | "Button-1":
                    return self.atualizar_contador(tecla)
                case _:
                    return 0


    def catch_comando(self, comando):
        # separando o comando em partes: numero de vezes a rodar e o comando
        def extrair_numeros(texto):
            numeros = re.findall(r'\d+', texto)
            if numeros:
                return int(''.join(numeros))
            else:
                return 1

        comando_sem_numeros = re.sub(r'\d', '', comando)
        numeros = extrair_numeros(comando)

        # tratando o comando de fato
        shortcuts.search_command(comando_sem_numeros, numeros, self.main_textarea)
        
        # apagando o comando enviado
        self.bottom_command_output.delete("1.0", ctk.END)
        return 0



    def atualizar_contador(self, e=None):
            
        self.vals = [int(label.cget("text")) for label in self.labels]
        print(self.vals)

        def add_zero_to_selected_line(self):
            # pegando o valor da linha selecionada dentre as visiveis
            self.label_value = self.get_visible_line(self.main_textarea)
            
            # definindo 0 na posicao atual do cursor
            self.labels[self.label_value - 1].configure(text=0)

            # se o cursor se moveu
            try:
                if self.last_zero_pos != self.label_value - 1:
                    self.labels[self.last_zero_pos].configure(text=1)
                    
            except Exception:
                self.labels[self.label_value - 2].configure(text=1)
                
                print("deu erro aqui")
            
            # guardando a posicao antiga do cursor
            self.last_zero_pos = self.label_value - 1

            calcular_distancias(self.vals, self.label_value -1)

        def calcular_distancias(array, posicao_zero):
            # Encontrar a posição do elemento 0
            # posicao_zero = array.index(0)
            
            # Calcular a distância entre cada elemento e o elemento 0
            distancias = [abs(i - posicao_zero) for i in range(len(array))]
            self.vals = distancias.copy()
            return distancias

        add_zero_to_selected_line(self)
        
        return 0
    
        def move_up(self):
            if 0 in [int(x) + 1 for x in self.num_to_labels]:
                self.num_to_labels = [int(x) + 1 for x in self.num_to_labels]
        
        # aqui eu subtraio 1 de cada elemento. Assim, o array move um pro lado. o antigo 1 vira 0, etc..
        def move_down(self):
            if 0 in [int(x) - 1 for x in self.num_to_labels]:
                self.num_to_labels = [int(x) - 1 for x in self.num_to_labels]

        def update_counter(self):
            for I, label in enumerate(self.labels):
                label.configure(text=self.num_to_labels[I])
        # pega a linha que deve ser mudada o label
        self.current_line = int(self.main_textarea.index(tk.INSERT).split('.')[0])




        def verificar_linha(self, numero_linha):
            conteudo = self.main_textarea.get(f"{numero_linha}.0", f"{numero_linha + 1}.0")
            return conteudo.strip()



        # se eu clicar em alguma linha
        if "ButtonPress" in str(e):            
            return 0


        # Ver se são linhas iguais
        try:
            if self.old_line == self.current_line:
                print("linhas iguais", e)

                # Caso vc esteja apagando algo na mesma linha
                if e == "BackSpace":
                    print("aq msmo")
                    if self.current_line == self.old_line:
                        return 0
                    return 0
                else:

                    if verificar_linha(self, self.current_line):
                        if self.old_line > self.current_line:
                            print("move pra cima")
                            move_up(self)
                            return update_counter(self)
                        elif self.old_line < self.current_line:
                            print("move pra baixo")
                            move_down(self)
                            return update_counter(self)
                        else:
                            print("nao faça nada")
                        pass
                    else:
                        return 0
                
            else:
                pass
        
        # Caso não tenha uma linha anterior (1° interação)
        except AttributeError:
            print("E: ",e)
            self.old_line = self.current_line
            
            if e == "Return":
                move_down(self)
                return update_counter(self)
            else:
                return 0
            
        # atualizar a linha anterior
        self.old_line = self.current_line        


        if e == "Down" or e == "Return":
            move_down(self)
            update_counter(self)

            return 0
        elif e == "Up":
            move_up(self)
            update_counter(self)
            return 0
        
        elif e == "BackSpace":
            print("aqui embaixo")
            move_up(self)
            update_counter(self)
            return 0

        else:
            return


        self.total_linhas = self.obter_numero_de_linhas()

        self.linhas_visiveis = self.calcular_numero_de_linhas_visiveis()

        self.teste = self.total_linhas - self.linhas_visiveis
        if self.teste >= 0:
            # isso é necessário porque senao o programa tenta usar um label que não existe
            self.current_line -= self.teste
            print("ta caindo aqui 2")

        print("TESTE:", self.teste)

        print("linha atual: ", self.current_line)

        if self.num_to_labels.count("ME") > 1:
            self.num_to_labels = [0 if label == "ME" else label for label in self.labels]
        
        try:
            if self.teste > 0:
                print("Erro aqui né?")
                self.num_to_labels[self.current_line - 2] = 0
                self.num_to_labels[self.current_line - 1] = "ME"
                self.num_to_labels[self.current_line] = 0
            else:
                self.num_to_labels[self.current_line - 2] = 0
                self.num_to_labels[self.current_line - 1] = "ME"
                self.num_to_labels[self.current_line] = 0

        except IndexError:
            print("Lidando com linhas abaixo!")
            print(self.num_to_labels)

            # se o ultimo elemento nao for o "ME"
            if self.num_to_labels[-1] != "ME":
                # o ultimo elemento se torna o "ME"
                self.num_to_labels[-1] = "ME"
                self.labels[self.total_linhas - 1].configure(text="ME")
                
                return 0
            
            # precisa deste else para ele trancar o numero 
            else:
                try:
                    print("Aqui")
                    self.labels[self.total_linhas - 1].configure(text="ME")
                    #self.num_to_labels = [int(x) + 1 for x in self.num_to_labels if isinstance(x, int) else "ME" for x in self.num_to_labels]
                    self.num_to_labels = [int(x) + 1 if isinstance(x, int) else "ME" for x in self.num_to_labels]
                    for I, label in enumerate(self.labels):
                        label.configure(text=self.num_to_labels[I])

                    print(self.num_to_labels)
                    return 0
                
                except IndexError:
                    print("Peido")
                    self.labels[-1].configure(text="ME")
                    self.labels[-2].configure(text="0")
                    self.num_to_labels[-2] = 0
                    return 0

        # distancia deles ate o elemento acima
        
        # Calcula a distância entre cada elemento e o elemento que se tornou 0
        for i in range(len(self.num_to_labels)):
            if self.num_to_labels[i] != "ME":
                distance = abs(self.current_line - 1 - i)
                self.num_to_labels[i] = distance
        
        for I, label in enumerate(self.labels):
            label.configure(text=self.num_to_labels[I])
        
        print(self.num_to_labels)

    def get_visible_line(self, text_widget):
        # Obtém a informação da linha atual
        cursor_pos = text_widget.index(tk.INSERT)
        line_number = int(cursor_pos.split('.')[0])
        
        # Calcula a primeira linha visível na tela
        first_visible_line = int(text_widget.index("@0,0").split('.')[0])
        
        # Calcula a linha visível atual
        visible_line = line_number - first_visible_line + 1
        
        print(visible_line)
        return visible_line

    
    def calcular_numero_de_linhas_visiveis(self):
        self.main_textarea.update_idletasks()  # Atualiza a geometria antes de calcular

        try:
            height = self.main_textarea.winfo_height()
            line_height = self.main_textarea.dlineinfo("1.0")[3]  # Altura da primeira linha
            visible_lines = height // line_height

            return visible_lines
        except TypeError:
            return self.max_linhas_visiveis


    def obter_numero_de_linhas(self):
        # Obtém o conteúdo do TextBox como uma string
        conteudo = self.main_textarea.get("1.0", "end-1c")

        # Divide a string em linhas usando '\n' como delimitador e conta o número de elementos
        numero_de_linhas = len(conteudo.split('\n'))
        print(numero_de_linhas)
        return numero_de_linhas


    def move_scroll(self):
        # Obtém o número da linha atual (linha onde o cursor está)
        current_line = int(self.main_textarea.index(tk.INSERT).split('.')[0])

        # Calcula a posição relativa da linha em relação ao número total de linhas
        relative_position = current_line / float(self.main_textarea.index("end").split('.')[0])

        # Move o scroll para a posição relativa da linha
        #self.main_textarea.yview_moveto(relative_position - 1)
        self.left_textarea.yview_moveto(relative_position - 1)
    
    def check_if_synced(self):
        pass



if __name__ == "__main__":
    root = ctk.CTk()
    app = MainApp(root)
    root.mainloop()