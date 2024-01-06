import json
import customtkinter as ctk

class UserConfig:
    def __init__(self, root):
        self.root = root
        self.main_app_instance = None

    def setup(self, gui):
         self.gui = gui
         self.maintext = self.gui.main_textarea
    
    def load_user_config(self):
        with open("config.json", "r") as file:
            self.config = json.load(file)
        
        self.selected_line_background_color = self.config["line_background_color"]
        self.programming_language_format = self.config["programming_language_format"]
        self.auto_insert_delimiters = self.config["auto_insert_delimiters"]

        print(self.config)
    

    def check_delimiter_chars(self, event, maintext):
        if self.config["auto_insert_delimiters"]:
                char_pressed = event.char
                
                dc = {
                    "[": "]",
                    "{": "}",
                    "(": ")",
                    '"': '"',
                    "'": "'"
                }

                if char_pressed in dc:
                    linha_atual = int(maintext.index(ctk.INSERT).split(".")[0])
                    coluna_atual = int(maintext.index(ctk.INSERT).split(".")[1])

                    maintext.insert(ctk.INSERT, dc[char_pressed])
                    maintext.mark_set(ctk.INSERT, f"{linha_atual}.{coluna_atual}")
                    return 0
    

    def check_char_for_language_format(self, tecla, char_anterior):
        match self.programming_language_format:
              case "Python":
                   match tecla.keysym:
                        case "Return":
                             #print("char anterior: ", char_anterior)
                             match char_anterior:
                                  case ":", "'", '"':
                                       self.adicionar_linha_com_tab(self.maintext)

                                  case "(" | "[" | "{" | '"' | "'" | ":":
                                       self.adicionar_linha_com_tab(self.maintext, extra_line=True)


    def adicionar_linha_com_tab(self, text_widget, extra_line = False):
        # Obtém a posição atual do cursor (marcador "insert")
        cursor_pos = text_widget.index(ctk.INSERT)

        # Divide a posição para obter o número da linha
        numero_linha = int(cursor_pos.split('.')[0])
        
        conteudo_linha_anterior = text_widget.get(f"{numero_linha-1}.0", f"{numero_linha - 1}.end")
        qtd_espacamentos = conteudo_linha_anterior.count("\t") + 1

        # Calcula a posição do início da próxima linha
        posicao_inicio_proxima_linha = f"{numero_linha}.0"

        if extra_line:
            # Insere uma nova linha abaixo da atual
            text_widget.insert(posicao_inicio_proxima_linha, '\n')

        # Calcula a posição do cursor na nova linha
        nova_posicao_cursor = f"{numero_linha}.0"

        # Insere um caractere de tabulação na nova linha
        text_widget.insert(nova_posicao_cursor, '\t'*qtd_espacamentos)
        text_widget.mark_set(ctk.INSERT, nova_posicao_cursor.split(".")[0] + ".end")
        linha_2 = f"{int(nova_posicao_cursor.split('.')[0]) + 1}.0" 
        print(linha_2)
        text_widget.insert(linha_2, '\t'*int(qtd_espacamentos - 1))
        self.gui.realcar_linha_selecionada()
        

