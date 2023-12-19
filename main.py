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
        
        self.trocar_modo(self.modo)
        self.labels = []
        self.create_labels()
        
        self.combo = []


    def create_labels(self):
        # Sem o update ele nao consegue calcular o num de linhas
        self.root.update()

        self.max_linhas_visiveis = self.calcular_numero_de_linhas_visiveis()
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

        self.root.rowconfigure(0, weight=1)

        # creating bottom frame
        self.bottomframe = ctk.CTkFrame(root)
        self.bottomframe.grid(row=1, column=0, columnspan=2, sticky="ew")


    def calcular_tamanho_caixa_de_texto(self):
        # precisa deste update para ele registrar o valor correto da resolução
        self.root.update()
        altura_janela = self.root.winfo_height()
        print(altura_janela)
        tam = self.root.winfo_height()
        print("mainframe h: ", self.mainframe.winfo_height())



        tamanho_fonte_ocupa = self.firacode.metrics()["linespace"] + 1

        # estranho isso, mas ta funcionando
        tam = self.mainframe.winfo_height()
        #tam = round(tam / tamanho_fonte_ocupa) * tamanho_fonte_ocupa
        tam = (int(str(self.mainframe.winfo_height())[0]) * 2)
        print("Tamanho: ", tam)
        tam *= tamanho_fonte_ocupa
        
        # assim eu consigo 10 linhas de espaço
        #tam = tamanho_fonte_ocupa * 10

        #tam = tamanho_fonte_ocupa * 10
        self.main_textarea.configure(height=(tam))



        stam_ultimo_char = int(str(tam)[-1])
        """
        
        if tam % 19 != 0:
            print("aumentar uma linha")
            tam = 37 * 3
            #tam = (((tam // 20) + 1) * 20) + 8
            #print("Novo tam neste caso: ", tam, tam/19)
        """
        self.main_textarea.configure(height=(tam))
        print("Tam: ", tam)
        self.ajustar_pady_primeiro_label_contador()


    def ajustar_pady_primeiro_label_contador(self):
        try:
            self.root.update()
            self.labels[0].configure(pady=0)
            
        # caso o contador nao tenha sido criado ainda
        except IndexError:
            return


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
        self.main_textarea.grid(row=0, column=0, sticky="ew", pady=(20,10))
        self.main_textarea.focus_set()

        


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
        

    def capture_commands(self):
        # ele envia argumentos mesmo sem indicar
        root.bind("<Key>", self.tecla_pressionada)
        root.bind("<Button-1>", self.atualizar_contador)
        #root.bind("<Escape>", lambda e: self.trocar_modo(self.modo))
        root.bind("<Escape>", self.atualizar_posicao_contador_por_resolucao)
        self.main_textarea.bind("<MouseWheel>", lambda e: "break")

    def teste(self):
        self.ok = 1
        return 1

    def configure_cases(self, e):
        print("Recebido")
        try:
            # caso a altura da janela atual seja diferente da antiga
            if self.root.winfo_height() != self.height_antigo:
                print("Arrumar janela")
                self.atualizar_posicao_contador_por_resolucao()
                    
        except Exception:
            self.height_antigo = e.height
            # caso o height antigo nao exista ainda

        self.height_antigo = e.height
        return 0
    
    def atualizar_posicao_contador_por_resolucao(self, e = None):
        return self.create_labels()

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
        def add_zero_to_selected_line(self):
            # pegando o valor da linha selecionada dentre as visiveis
            self.label_value = self.get_visible_line(self.main_textarea)

            print("qtd_labels: ", len(self.labels), "qtd linhas visiveis: ", self.calcular_numero_de_linhas_visiveis(),
                  "linha visivel atual: ", self.label_value)
            
            if int(self.label_value) > len(self.labels):
                self.label_value -= 1

            else:
                self.labels[self.label_value - 1].configure(text=0)

                """
                print("adicionando um numero label")
                label = ctk.CTkLabel(self.leftframe, text=9, font=self.firacode)
                label.grid(row=len(self.labels), column=0, sticky="en", pady=(0))
                self.labels.append(label)

                tamanho = self.main_textarea.winfo_height()
                print("tamanho: ", tamanho)
                self.main_textarea.configure(height=int(tamanho) + 40)
                """

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
        print(line_number)
        
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
            return visible_lines

        except TypeError:
            return self.max_linhas_visiveis


    def obter_numero_de_linhas(self):
        # Obtém o conteúdo do TextBox como uma string
        conteudo = self.main_textarea.get("1.0", "end-1c")

        # Divide a string em linhas usando '\n' como delimitador e conta o número de elementos
        numero_de_linhas = len(conteudo.split('\n'))
        return numero_de_linhas


    def move_scroll(self):
        # Obtém o número da linha atual (linha onde o cursor está)
        current_line = int(self.main_textarea.index(tk.INSERT).split('.')[0])

        # Calcula a posição relativa da linha em relação ao número total de linhas
        relative_position = current_line / float(self.main_textarea.index("end").split('.')[0])

        # Move o scroll para a posição relativa da linha
        self.left_textarea.yview_moveto(relative_position - 1)
    

if __name__ == "__main__":
    root = ctk.CTk()
    app = MainApp(root)
    root.mainloop()