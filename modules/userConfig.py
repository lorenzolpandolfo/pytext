import json
import customtkinter as ctk

class UserConfig:
    def __init__(self, mainApp):
        self.main_app_instance = mainApp
        self.root = mainApp.root
        self.load()


    def setup(self, gui):
         self.gui = gui
         self.maintext = self.gui.main_textarea


    def load(self):
        with open("config.json", "r") as file:
            self.config = json.load(file)
        
        self.selected_line_background_color     = self.config["line_background_color"]
        self.programming_language_format        = self.config["programming_language_format"]
        self.auto_insert_delimiters             = self.config["auto_insert_delimiters"]

        self.font                               = self.config["font"]
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
                    actual_index = maintext.index(ctk.INSERT)

                    actual_line = int(actual_index.split(".")[0])
                    actual_column = int(actual_index.split(".")[1])

                    maintext.insert(ctk.INSERT, dc[char_pressed])
                    maintext.mark_set(ctk.INSERT, f"{actual_line}.{actual_column}")
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
        cursor_pos = text_widget.index(ctk.INSERT)

        numero_linha = int(cursor_pos.split('.')[0])
        
        conteudo_linha_anterior = text_widget.get(f"{numero_linha-1}.0", f"{numero_linha - 1}.end")
        qtd_espacamentos = conteudo_linha_anterior.count("\t") + 1

        # Calcula a posição do início da próxima linha
        posicao_inicio_proxima_linha = f"{numero_linha}.0"

        if extra_line:
            # insert a new line below the current line
            text_widget.insert(posicao_inicio_proxima_linha, '\n')

        # set the cursor to the new line
        nova_posicao_cursor = f"{numero_linha}.0"

        # add a \t to the new line
        text_widget.insert(nova_posicao_cursor, '\t'*qtd_espacamentos)
        text_widget.mark_set(ctk.INSERT, nova_posicao_cursor.split(".")[0] + ".end")

        linha_2 = f"{int(nova_posicao_cursor.split('.')[0]) + 1}.0" 
        text_widget.insert(linha_2, '\t'*int(qtd_espacamentos - 1))
        self.gui.realcar_linha_selecionada()
        

