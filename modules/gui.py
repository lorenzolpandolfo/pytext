import customtkinter as ctk
import math
import json
from modules.CTkEasyTextBox import CTkEasyTextBox

class GUI:
    def __init__(self, main_app_instance):
        self.main_app_instance = main_app_instance
        self.root = main_app_instance.root

        self.Font = self.main_app_instance.Font
        self.Counter = self.main_app_instance.Counter
        self.buffer_content = ""

        self.labels = []
    

    def setup(self, command_manager_instance, user_config_instance):
        self.command_manager_instance = command_manager_instance
        self.user_config_instance = user_config_instance


    def write_another_file_content(self, content:str):
        self.main_textarea.configure(state="normal")
        self.main_textarea.delete("1.0", "end")
        self.main_textarea.insert(ctk.END, content)
        self.main_textarea.configure(state="disabled")


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

        #print(maximo_linhas_total)

        min = int((maximo_linhas_total / 10) * 3)
        max = int((maximo_linhas_total / 10) * 7)


        #print(linha_visivel, min, max, maximo_linhas_total)

        if linha_visivel <= min:
            #print("Subindo")
            self.main_textarea.yview_scroll(-1, "units")
        elif linha_visivel >= max:
            #print("Descendo")
            self.main_textarea.yview_scroll(1, "units")

    def inserir(self, texto):
        return self.main_textarea.insert("1.0", texto)

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

    
    def obter_maximo_coluna_por_linha(self):
        pass


    def obter_numero_de_colunas_atual(self):
        linha = self.main_textarea.get(ctk.INSERT+" linestart", ctk.INSERT+" lineend")
        colunas = len(linha)
        return colunas


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
        self.Counter.create_labels()


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


    def create_widgets(self):
        # initializing main text area
        # fazer com que ele tenha um tamanho sempre multiplo do tamanho das linhas
        #self.main_textarea = ctk.CTkTextbox(self.mainframe, wrap=ctk.WORD, font=self.Font.font, height=0)
        self.main_textarea = CTkEasyTextBox(self.mainframe, wrap=ctk.WORD, font=self.Font.font, height=0)
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

