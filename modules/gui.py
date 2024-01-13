import customtkinter as ctk
import math
import json
from modules.CTkEasyTextBox import CTkEasyTextBox
import os

class GUI:
    def __init__(self, main_app_instance):
        self.main_app_instance = main_app_instance
        self.root = main_app_instance.root

        self.Font = self.main_app_instance.Font
        self.Counter = self.main_app_instance.Counter
        self.buffer_content = ""
        self.labels = []

        # resolution auto sizing
        self.can_adjust = True
        self.lastheight = 0

    def setup(self, command_manager_instance, user_config_instance):
        self.command_manager_instance = command_manager_instance
        self.user_config_instance = user_config_instance


    def write_another_file_content(self, content:str, file_name:str, auto_insert:bool = False):
        self.main_app_instance.File.pos_per_dir.append(self.main_textarea.index(ctk.INSERT))
        self.main_textarea.configure(state="normal")
        self.main_textarea.delete("1.0", "end")
        self.main_textarea.insert(ctk.END, content)
        self.main_textarea.configure(state="disabled")
        self.main_textarea.mark_set(ctk.INSERT, "1.0")
        self.realcar_linha_selecionada()
        self.main_app_instance.File.file_name = file_name
        self.main_app_instance.Counter.atualizar_contador()
        self.root.update()
        if file_name == "":
            self.bottom_current_dir.configure(text=self.main_app_instance.File.get_formatted_to_gui_cur_dir(self.main_app_instance.File.terminal_directory,"Unnamed"))
        else: self.bottom_current_dir.configure(text=self.main_app_instance.File.get_formatted_to_gui_cur_dir(self.main_app_instance.File.terminal_directory, self.main_app_instance.File.file_name))

        if "." in file_name:
            file_extension = file_name.split(".")[1]

            match file_extension:
                case "py":
                    language = "python"
                case _:
                    print(f".{file_extension} syntax highlight is not supported yet")
                    self.main_textarea._syntax_rules_loaded = False
                    language = False

            if language:
                os.chdir(os.path.dirname(os.path.abspath(__file__)))
                os.chdir("..")
                full_language_path = os.path.join(os.getcwd(), "languages", language)
                self.main_textarea.load_syntax_rules(os.path.join(full_language_path, "syntax.json"), os.path.join(full_language_path,"syntax_colors.json"))
                self.main_textarea.active_syntax_highlighting()
        
        if auto_insert:
            # ver pq q tem q ter 2 vezes
            self.command_manager_instance.trocar_modo(self.main_app_instance.modo)
            self.command_manager_instance.trocar_modo(self.main_app_instance.modo)



    def realcar_linha_selecionada(self, *args):
        texto = self.main_textarea
        linha_atual = int(texto.index(ctk.INSERT).split(".")[0])
        inicio_linha = f"{linha_atual}.0"
        fim_linha = f"{linha_atual + 1}.0"
        
        texto.tag_remove("realce", "1.0", ctk.END)
        texto.tag_add("realce", inicio_linha, fim_linha)
        texto.tag_config("realce", background=self.user_config_instance.theme["line_background_color"])


    def mover_tela(self, move_to_center = False):
        linha_visivel = int(self.Counter.get_visible_line(self.main_textarea))
        maximo_linhas_total = len(self.Counter.labels)


        min = int((maximo_linhas_total / 10) * 3)
        max = int((maximo_linhas_total / 10) * 7)

        # in this case, user needs to move the current screen position to the center
        if move_to_center:
            lines_to_move = 0

            while linha_visivel <= min:
                lines_to_move -= 1
                linha_visivel += 1
                
            
            while linha_visivel >= max:
                lines_to_move += 1
                linha_visivel -= 1
            
            return self.main_textarea.yview_scroll(lines_to_move, "units")
        
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


    def obter_numero_de_colunas_atual(self):
        linha = self.main_textarea.get(ctk.INSERT+" linestart", ctk.INSERT+" lineend")
        colunas = len(linha)
        return colunas


    def obter_numero_de_linhas_e_colunas(self, formatted_to_gui = False):
        # Obtém o conteúdo do TextBox como uma string
        conteudo = self.main_textarea.get("1.0", "end-1c")
        linhas = conteudo.split('\n')
        
        numero_de_linhas = len(linhas)

        # maior valor de comprimento de linha por cada linha
        num_colunas = max(len(linha) for linha in linhas)
        return (numero_de_linhas, num_colunas) if not formatted_to_gui else f"{numero_de_linhas}L, {num_colunas}C"

    def update_labels_to_current_resolution(self, *args):
        self.Counter.create_counter()
        self.Counter.create_labels()
        return self.root.after(700, self.make_label_update_available)


    def make_label_update_available(self):
        # serve basicamente para redefinir a variavel ok para 1, para que seja possivel
        # reatualizar a resolução
        self.can_adjust = True
        print("can adjust: ", self.can_adjust)
        print('definindo para: ', self.root.winfo_height())
        self.lastheight = self.root.winfo_height()


    def adjust_widgets_to_resolution(self, *args):
        if int(self.root.winfo_height()) == int(self.lastheight):
            pass
        elif self.can_adjust:
            self.can_adjust = False
            # print("resolution changed")
            self.update_labels_to_current_resolution()



    def start(self):
        self.create_window()
        self.create_frames()
        self.create_widgets()
        self.Counter.create_counter()
        self.Counter.create_labels()


    def create_window(self):
        self.root.geometry(f"{self.user_config_instance.config["window"]["width"]}x{self.user_config_instance.config["window"]["height"]}")
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
        self.main_textarea = CTkEasyTextBox(self.mainframe, wrap=ctk.WORD, font=self.Font.font, height=0)
        self.main_textarea.grid(row=0, column=0, sticky="new", padx=10, pady=(20, 10))
        self.main_textarea.focus_set()
        self.main_textarea.grid_rowconfigure(0, weight=1)
        self.main_textarea.configure(state="disabled", tabs=(self.main_app_instance.Font.font.measure(" ") *self.user_config_instance.config["tab_width"],))
        
        # escondendo a barra de scroll
        theme_mode = ctk.get_appearance_mode()
        themes = {
            "Dark": "#1d1e1e",
            "Light": "#f9f9fa"
        }
        self.main_textarea.configure(yscrollcommand="", scrollbar_button_color=themes[theme_mode], scrollbar_button_hover_color=themes[theme_mode])


        # configurando o mainframe
        self.mainframe.columnconfigure(0, weight=1)
        self.mainframe.rowconfigure(0, weight=1)

        # configurando o leftframe
        self.leftframe.columnconfigure(0, weight=0)
        self.leftframe.rowconfigure(0, weight=0)

        # creating the bottom label
        self.bottom_output_mode = ctk.CTkLabel(self.bottomframe, text=self.main_app_instance.modo, justify="center", font=self.Font.font)
        self.bottom_output_mode.grid(row=1, column=0, sticky="ew", columnspan=2)

        self.bottom_current_dir = ctk.CTkLabel(self.bottomframe, text="loading...", font=self.Font.gui_font)
        self.bottom_current_dir.grid(row=2,column=1, sticky="w", padx=10, pady=0)

        # creating the detailed command output label 
        self.bottom_output_detail = ctk.CTkLabel(self.bottomframe, text="", justify="left", font=self.Font.gui_font)
        self.bottom_output_detail.grid(row=2, column=1, sticky="e", padx=10)

        # creating the absolute line and column label
        self.doc_abs_line_and_columns = ctk.CTkLabel(self.bottomframe, text=self.obter_numero_de_linhas_e_colunas(formatted_to_gui=True), justify="left", font=self.Font.gui_font)
        self.doc_abs_line_and_columns.grid(row=2, column=0, sticky="e", padx=10)


        # Criando o textbox no segundo grid
        self.bottom_command_output = ctk.CTkTextbox(self.bottomframe, font=self.Font.gui_font, width=100, height=1)
        # Como o sticky é "e", ele vai ser ancorado para o leste ->
        self.bottom_command_output.grid(row=2, column=2, sticky="e", padx=(0, 10), pady=(0, 5))

        # o peso é 1 para que ele se mova para a direita
        self.bottomframe.columnconfigure(1, weight=1)
        # Configurando o textbox para ser menor verticalmente
        self.bottom_command_output.rowconfigure(1, weight=0)  # Ajuste para tornar a segunda linha menor

