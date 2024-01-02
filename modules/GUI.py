import customtkinter as ctk
import math
import json

class GUI:
    def __init__(self, main_app_instance):
        self.main_app_instance = main_app_instance
        self.root = main_app_instance.root

        self.Font = self.main_app_instance.Font
        self.Counter = self.main_app_instance.Counter

        self.labels = []
    

    def setup(self, command_manager_instance, user_config_instance):
        self.command_manager_instance = command_manager_instance
        self.user_config_instance = user_config_instance


    def create_counter(self, e = None):
        # Sem o update ele nao consegue calcular o num de linhas
        self.root.update()
        self.on_resize()
        self.max_linhas_visiveis = self.calcular_numero_de_linhas_visiveis()
        self.main_textarea._textbox.configure(height=self.max_linhas_visiveis)






    def calcular_tamanho_caixa_de_texto(self):
        # precisa deste update para ele registrar o valor correto da resolução
        self.root.update()
        altura_janela = self.root.winfo_height()
        #print(altura_janela)
        tam = self.root.winfo_height()
        # estranho isso, mas ta funcionando
        tam = tam/1.4
        #print("Tamanho no frame: ", self.mainframe.winfo_height(), "Tam: ", tam)

        print("Tamanho do texto alterado")



    def realcar_linha_selecionada(self, *args):
        texto = self.main_textarea
        linha_atual = int(texto.index(ctk.INSERT).split(".")[0])
        inicio_linha = f"{linha_atual}.0"
        fim_linha = f"{linha_atual + 1}.0"
        
        texto.tag_remove("realce", "1.0", ctk.END)
        texto.tag_add("realce", inicio_linha, fim_linha)
        texto.tag_config("realce", background=self.user_config_instance.selected_line_background_color)


    def mover_tela(self):
        linha_visivel = int(self.Counter.get_visible_line(self.main_textarea))
        maximo_linhas_total = len(self.Counter.labels)

        print(maximo_linhas_total)

        min = int((maximo_linhas_total / 10) * 3)
        max = int((maximo_linhas_total / 10) * 7)


        print(linha_visivel, min, max, maximo_linhas_total)

        if linha_visivel <= min:
            print("Subindo")
            self.main_textarea.yview_scroll(-1, "units")
        elif linha_visivel >= max:
            print("Descendo")
            self.main_textarea.yview_scroll(1, "units")


    def obter_caractere_anterior(self, text_widget, enter = False):
        if enter:
            # Obtém a posição atual do cursor (marcador "insert")
            cursor_pos = text_widget.index(ctk.INSERT)

            # Divide a posição para obter o número da linha e a coluna
            numero_linha, coluna = map(int, cursor_pos.split('.'))

            # Se estamos na primeira linha, não há linha acima para obter o último caractere
            if numero_linha <= 1:
                return None

            # Calcula a posição do último caractere da linha anterior
            posicao_ultimo_caractere_linha_anterior = f"{numero_linha - 1}.end - 1 char"

            # Obtém o último caractere da linha anterior
            ultimo_caractere_linha_anterior = text_widget.get(posicao_ultimo_caractere_linha_anterior)

            return ultimo_caractere_linha_anterior
        else:
            # Obtém a posição atual do cursor (marcador "insert")
            cursor_pos = text_widget.index(ctk.INSERT)

            # Calcula a posição do caractere anterior
            posicao_anterior = f"{cursor_pos} - 1 char"

            # Obtém o caractere anterior
            caractere_anterior = text_widget.get(posicao_anterior, cursor_pos)
            
        return caractere_anterior

    def atualizar_contador(self, e=None):
        def add_zero_to_selected_line(self):
            # pegando o valor da linha selecionada dentre as visiveis
            self.label_value = self.get_visible_line(self.main_textarea)

            try:
                self.labels[self.label_value - 1].configure(text=999)
            except IndexError:
                print("linha cortada para tentar evitar dessincronização de contador")
                # 250 tira duas linhas, considerando tamanhos extras do widget
                #self.main_textarea.configure(height=int(self.main_textarea.winfo_height()) - 200)

            # se o cursor se moveu
            try:
                if self.last_zero_pos != self.label_value - 1:
                    self.labels[self.last_zero_pos].configure(text=1)
                    
            except Exception:
                self.labels[self.label_value - 2].configure(text=1)
                
            
            # guardando a posicao antiga do cursor
            self.last_zero_pos = self.label_value - 1

            return calcular_distancias([label.cget("text") for label in self.labels], self.label_value -1)


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

        print("wid: ", 2*(self.main_textarea.winfo_width()/self.Font.size))
        # se a linha de baixo for a linha atual (linha grande quebrada em 2)
        if self.obter_numero_de_colunas_atual() > 2.2*(self.main_textarea.winfo_width()/self.Font.size):
            print("linha grande")
            for i, label in enumerate(self.labels):
                if label.cget("text") == 1:
                    self.labels[i + 2].configure(text="")
                    break

        if self.obter_numero_de_colunas_atual() > 999999:
            for i, label in enumerate(self.labels):
                if label.cget("text") == 1:
                    self.labels[i + 2].configure(text="")
                    break

        return 0
    
    def obter_maximo_coluna_por_linha(self):
        pass


    def calcular_numero_de_linhas_visiveis(self):
        self.main_textarea.update_idletasks()  # Atualiza a geometria antes de calcular
        self.main_textarea.update()
        #self.calcular_tamanho_caixa_de_texto()

        try:
            height = self.main_textarea.winfo_height()
            line_height = self.main_textarea.dlineinfo("1.0")[3]  # Altura da primeira linha
            visible_lines = height // line_height
            #print("num de linhas calculado")
            return visible_lines

        except TypeError:
            print("nao consegui contar")
            # cuidar aqui, isso pode nao funcionar. Fazer testes para encontrar a fonte desse erro
            self.root.configure(height=int(self.root.winfo_height()) - self.Font.size)
            return self.max_linhas_visiveis


    def obter_numero_de_colunas_atual(self):
        linha = self.main_textarea.get(ctk.INSERT+" linestart", ctk.INSERT+" lineend")
        colunas = len(linha)
        return colunas


    def obter_numero_de_linha_atual(self, c = 0):
        num_linha = int(self.main_textarea.index(ctk.INSERT).split(".")[0])
        num_linha += c
        print(num_linha)
        return num_linha


    def obter_numero_de_linhas_e_colunas(self, f = False):
        # Obtém o conteúdo do TextBox como uma string
        conteudo = self.main_textarea.get("1.0", "end-1c")
        linhas = conteudo.split('\n')
        
        numero_de_linhas = len(linhas)

        # maior valor de comprimento de linha por cada linha
        num_colunas = max(len(linha) for linha in linhas)
        
        if not f:
            return (numero_de_linhas, num_colunas)
        else:
            return f"{numero_de_linhas}L, {num_colunas}C"


    def teste(self, *args):
        #self.create_counter()
        #self.create_labels()
        

        self.Counter.create_counter()
        self.Counter.create_labels()
        
        return self.root.after(1000, self.a)


    def a(self):
        # serve basicamente para redefinir a variavel ok para 1, para que seja possivel
        # reatualizar a resolução
        self.command_manager_instance.ok = 1
        print("ok definido: ", self.command_manager_instance.ok)
        print('definindo para: ', self.root.winfo_height())
        self.command_manager_instance.lastheight = self.root.winfo_height()


    def start(self):
        self.create_window()
        self.create_frames()
        self.create_widgets()
        self.Counter.create_counter()
        #self.create_counter()
        self.Counter.create_labels()
        #self.create_labels()
        #print("Num labels: ", len(self.labels))


    def create_window(self):
        self.root.geometry("1100x749")
        self.root.title("The Pytext Editor")


    def create_frames(self):
        # creating left frame
        self.leftframe = ctk.CTkFrame(self.root)
        self.leftframe.grid(row=0, column=0, sticky="ns")
        # peso 0 para não expandir (janela)
        self.root.columnconfigure(0, weight=0)

        # creating the main frame
        self.mainframe = ctk.CTkFrame(self.root)
        self.mainframe.grid(row=0, column=1, sticky="new")
        # peso 1 para que ele expanda (janela)
        self.root.columnconfigure(1, weight=1)
        self.root.rowconfigure(0, weight=1)

        # creating bottom frame
        self.bottomframe = ctk.CTkFrame(self.root)
        self.bottomframe.grid(row=1, column=0, columnspan=2, sticky="ew")


    def on_resize(self, e=None):
        # testando aqui um valor alto para ele ajustar depois
        altura_janela = self.root.winfo_height() * 2

        print("Altura: ",altura_janela)
        # Calcula o número de linhas visíveis desejado
        num_linhas_visiveis = altura_janela // self.Font.size

        print(num_linhas_visiveis)

        # Configura a altura do widget Text em pixels, garantindo que seja um múltiplo do font_size
        self.main_textarea._textbox.configure(height=num_linhas_visiveis)
        self.calcular_numero_de_linhas_visiveis()


    def create_widgets(self):
        # initializing main text area
        # fazer com que ele tenha um tamanho sempre multiplo do tamanho das linhas
        self.main_textarea = ctk.CTkTextbox(self.mainframe, wrap=ctk.WORD, font=self.Font.font, height=0)
        self.main_textarea.grid(row=0, column=0, sticky="new", padx=10, pady=(20, 10))
        self.main_textarea.focus_set()
        self.main_textarea.grid_rowconfigure(0, weight=1)


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
        self.left_textarea = ctk.CTkTextbox(self.leftframe, width=70, wrap=ctk.CHAR, font=self.Font.font)
        #self.left_textarea.grid(row=0, column=0, sticky="ns", padx=(10,10), pady=(20,10))

        # configurando o leftframe
        self.leftframe.columnconfigure(0, weight=0)
        self.leftframe.rowconfigure(0, weight=0)

        # creating the bottom label
        self.bottom_output_mode = ctk.CTkLabel(self.bottomframe, text=self.main_app_instance.modo, justify="center", font=self.Font.font)
        self.bottom_output_mode.grid(row=1, column=0, sticky="ew", columnspan=2)

        self.bottom_output_detail = ctk.CTkLabel(self.bottomframe, text="", justify="left", font=self.Font.font)
        self.bottom_output_detail.grid(row=1, column=1, sticky="e", padx=10)
        self.bottom_output_doc_info = ctk.CTkLabel(self.bottomframe, text=self.obter_numero_de_linhas_e_colunas(f=True), justify="left", font=self.Font.font)
        self.bottom_output_doc_info.grid(row=1, column=0, sticky="e", padx=10)
        # Criando o textbox no segundo grid
        self.bottom_command_output = ctk.CTkTextbox(self.bottomframe, font=self.Font.font, width=100, height=2)
        # Como o sticky é "e", ele vai ser ancorado para o leste ->
        self.bottom_command_output.grid(row=1, column=2, sticky="e", padx=(0, 10), pady=(0, 5))

        # o peso é 1 para que ele se mova para a direita
        self.bottomframe.columnconfigure(1, weight=1)
        # Configurando o textbox para ser menor verticalmente
        self.bottom_command_output.rowconfigure(1, weight=0)  # Ajuste para tornar a segunda linha menor

