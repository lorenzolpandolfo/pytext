import customtkinter as ctk
import math


class GUI:
    def __init__(self, root):
        self.root = root
        self.labels = []
    

    def setup(self, main_app_instance, command_manager_instance):
        self.main_app_instance = main_app_instance
        self.command_manager_instance = command_manager_instance


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


    def create_labels(self):
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
        linha_atual = int(texto.index(ctk.INSERT).split(".")[0])
        inicio_linha = f"{linha_atual}.0"
        fim_linha = f"{linha_atual + 1}.0"
        
        texto.tag_remove("realce", "1.0", ctk.END)
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
                #self.main_textarea.configure(height=int(self.main_textarea.winfo_height()) - 200)

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
        cursor_pos = text_widget.index(ctk.INSERT)
        line_number = int(cursor_pos.split('.')[0])
        
        # Calcula a primeira linha visível na tela
        first_visible_line = int(text_widget.index("@0,0").split('.')[0])
        
        # Calcula a linha visível atual
        visible_line = line_number - first_visible_line + 1
        
        return visible_line


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
            return self.max_linhas_visiveis


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


    def teste(self, e = None):
        self.create_counter()
        self.create_labels()


    def start(self):
        self.create_window()
        self.create_frames()
        self.create_widgets()
        self.create_counter()
        self.create_labels()
        print("Num labels: ", len(self.labels))


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
        font_size = self.firacode.metrics()['linespace']
        # testando aqui um valor alto para ele ajustar depois
        altura_janela = self.root.winfo_height() * 2

        print("Altura: ",altura_janela)
        # Calcula o número de linhas visíveis desejado
        num_linhas_visiveis = altura_janela // font_size

        print(num_linhas_visiveis)

        # Configura a altura do widget Text em pixels, garantindo que seja um múltiplo do font_size
        self.main_textarea._textbox.configure(height=num_linhas_visiveis)
        self.calcular_numero_de_linhas_visiveis()



    def create_widgets(self):
        # initializing firacode font
        src = r"fonts\firacode.ttf"
        # carrega a fonte
        ctk.FontManager.load_font(src)
        # agora ele reconhece a family Fira Code, porque eu carreguei antes
        self.firacode = ctk.CTkFont(family="Fira Code", size=19) 

        # initializing main text area
        # fazer com que ele tenha um tamanho sempre multiplo do tamanho das linhas
        self.main_textarea = ctk.CTkTextbox(self.mainframe, wrap=ctk.WORD, font=self.firacode, height=0)
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
        self.bottom_output_doc_info = ctk.CTkLabel(self.bottomframe, text=self.obter_numero_de_linhas_e_colunas(f=True), justify="left", font=self.firacode)
        self.bottom_output_doc_info.grid(row=1, column=0, sticky="e", padx=10)
        # Criando o textbox no segundo grid
        self.bottom_command_output = ctk.CTkTextbox(self.bottomframe, font=self.firacode, width=100, height=2)
        # Como o sticky é "e", ele vai ser ancorado para o leste ->
        self.bottom_command_output.grid(row=1, column=2, sticky="e", padx=(0, 10), pady=(0, 5))

        # o peso é 1 para que ele se mova para a direita
        self.bottomframe.columnconfigure(1, weight=1)
        # Configurando o textbox para ser menor verticalmente
        self.bottom_command_output.rowconfigure(1, weight=0)  # Ajuste para tornar a segunda linha menor

