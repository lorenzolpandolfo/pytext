
import customtkinter as ctk
from modules.shortcuts import Shortcuts
import re

class CommandManager:
    def __init__(self, main_app_instance):
        self.main_app_instance = main_app_instance
        self.root = main_app_instance.root


    def setup(self, gui_instance, user_config_instance, Counter):
        self.gui = gui_instance

        self.maintext = self.gui.main_textarea
        self.bottom_command_output = self.gui.bottom_command_output
        self.user_config_instance = user_config_instance
        self.Counter = Counter


    def capture_keybinds(self):
        self.root.bind("<Key>", self.tecla_pressionada)
        self.root.bind("<KeyRelease>", self.atualizar_contador_de_linhas_e_colunas_globais)
        self.root.bind("<Escape>", lambda _: self.escape_deal())
        # Atualizar as labels para ajustar na resolução
        self.root.bind("<Prior>", lambda e          : self.gui.update_labels_to_current_resolution(e))
        self.root.bind("<Configure>", lambda e      : self.gui.adjust_widgets_to_resolution(e))
        self.root.bind("<<Undo>>", lambda _      : self.gui.update_gui_to_current_text("text undo loaded to last separator"))
        self.root.bind("<<Redo>>", lambda _      : self.gui.update_gui_to_current_text("text redo loaded to last separator"))
        self.root.bind("<<Paste>>", lambda _      : self.gui.update_gui_to_current_text("paste event"))
        self.root.bind("<<Cut>>", lambda _      : self.gui.update_gui_to_current_text("cut event"))
        self.maintext.bind("<MouseWheel>", lambda _ : "break")


    def escape_deal(self):
        # if you're in a localdir Open file
        if self.main_app_instance.FileManager.file_name == "__pytextLocaldir__":
            updir = self.main_app_instance.FileManager.get_up_directory()
            self.main_app_instance.FileManager.open_local_directory_or_file(updir, self.maintext, self.main_app_instance, self.gui, updir = True)
        
        else:
            self.trocar_modo(self.main_app_instance.modo)


    def atualizar_contador_de_linhas_e_colunas_globais(self, *args):
        return self.gui.doc_abs_line_and_columns.configure(text=self.gui.obter_numero_de_linhas_e_colunas(formatted_to_gui=True))


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
        #print(self.main_app_instance.modo)
        return self.gui.bottom_output_mode.configure(text=self.main_app_instance.modo)


    def tecla_pressionada(self, event):
        
        self.gui.realcar_linha_selecionada(self.gui)
        tecla = event.keysym

        if self.main_app_instance.modo == "view":
            comando = self.bottom_command_output.get("1.0", "end-1c")

            # auto select files in directory viewer with the event char
            if self.main_app_instance.FileManager.file_name == "__pytextLocaldir__" and event.char.isalpha() and str(self.gui.main_textarea) in str(self.root.focus_get()):
                content = self.gui.main_textarea.get("1.0", ctk.END).splitlines()
                for i, line in enumerate(content):
                    if "▼ " in line: line = line.replace("▼ ", "")
                
                    linha_atual = int(self.gui.main_textarea.index(ctk.INSERT).split(".")[0])
                    current_line = self.gui.main_textarea.get(ctk.INSERT+" linestart", ctk.INSERT+" lineend")
                    if "▼ " in current_line: current_line = current_line.replace("▼ ", "")
                    
                    if event.char == current_line[0]:
                        max_linhas = self.gui.obter_numero_de_linhas_e_colunas()[0]

                        # if there is a next line
                        if int(linha_atual) + 1 <= max_linhas:
                            next_line = self.gui.main_textarea.get(f"{int(linha_atual) + 1}.0 linestart", f"{int(linha_atual) + 1}.0 lineend").replace("▼ ", "")
                            previous_line = self.gui.main_textarea.get(f"{int(linha_atual) - 1}.0 linestart", f"{int(linha_atual) - 1}.0 lineend").replace("▼ ", "")
                        
                            if next_line[0] == event.char:
                                position = int(linha_atual) + 1 if int(linha_atual) + 1 <= max_linhas else int(linha_atual) - 1
                            elif previous_line[0] == event.char:
                                position = self.first_occurrence
                            else:
                                self.gui.bottom_output_detail.configure(text=f"no other file starting with {event.char}")
                                break
                        else: position = self.first_occurrence

                        self.gui.main_textarea.mark_set(ctk.INSERT, f"{position}.0") 
                        self.gui.update_gui_to_current_text("")
                        break

                    if line[0] == event.char:
                        # saving the first occurrence of the char pressed
                        self.first_occurrence = f"{i + 1}"
                        self.gui.main_textarea.mark_set(ctk.INSERT, f"{i + 1}.0")
                        self.gui.update_gui_to_current_text("")
                        break

                    if i == len(content) - 1: self.gui.bottom_output_detail.configure(text=f"no file starting with {event.char}")


            
            # Caso não haja comandos e aperte :
            if comando == "":
                if tecla == "colon":
                    self.bottom_command_output.focus_set()


                elif tecla == "Return":
                    if self.main_app_instance.FileManager.file_name == "__pytextLocaldir__":
                        posicao_linha_atual = self.gui.main_textarea.index(ctk.INSERT).split('.')[0]
                        conteudo_linha_atual = self.gui.main_textarea.get(f"{posicao_linha_atual}.0", f"{posicao_linha_atual}.end")
                        self.main_app_instance.FileManager.open_local_directory_or_file(conteudo_linha_atual, self.maintext, self.main_app_instance, self.gui)
                    return
                
                else:
                    match tecla:
                        case "i":
                            if not self.main_app_instance.FileManager.file_name == "__pytextLocaldir__":
                                return self.trocar_modo(self.main_app_instance.modo)
                        
                        case "Up" | "Down" | "Left" | "Right" | "Return" | "BackSpace" | "Button-1":
                            self.gui.mover_tela()
                            self.Counter.atualizar_contador(tecla)
                        
                        
                        case _:
                            return 0

            # Caso aperte Enter para registrar o comando
            elif tecla == "Return":
                self.catch_command(comando)
                self.maintext.focus_set()
 

        elif self.main_app_instance.modo == "insert":
            # checa se é um delimitador
            self.user_config_instance.check_delimiter_chars(event, self.maintext)    
            caracteres_e_situacoes_em_python = [
                '\r',
                ' ', '.', ','
                '(', ')', '[', ']', '{', '}',
                ':', ',',
                "'", '"',
                '+', '-', '*', '/', '\\', '%',
                '<',  '>', 
                '=',
            ]

            if event.char in caracteres_e_situacoes_em_python:
                self.gui.main_textarea.edit_separator()

            match tecla:
                case "Up" | "Down" | "Left" | "Right" | "BackSpace" | "Button-1":
                    self.gui.mover_tela()
                    self.Counter.atualizar_contador(tecla)


                case "Return":
                    self.user_config_instance.check_char_for_language_format(event, self.gui.obter_caractere_anterior(self.maintext, enter=True))
                    return self.Counter.atualizar_contador(tecla)


                case _:
                    return 0


    def catch_command(self, comando):
        # separando o comando em partes: numero de vezes a rodar e o comando
        def extrair_numeros(texto):
            numeros = re.findall(r'\d+', texto)
            if not numeros: return 0
            return int(''.join(numeros))

        comando_sem_numeros = re.sub(r'\d', '', comando)
        numeros = extrair_numeros(comando)

        # tratando o comando de fato
        command_output = Shortcuts.search_command(comando_sem_numeros, numeros, self.maintext, self.main_app_instance, self.gui)

        if command_output == "sair":
            self.root.destroy()
            exit()
        else:
            self.gui.bottom_output_detail.configure(text=command_output)
            self.Counter.atualizar_contador()
            self.gui.realcar_linha_selecionada()

            # apagando o comando enviado
            self.bottom_command_output.delete("1.0", ctk.END)
            return 0
