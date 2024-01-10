
import customtkinter as ctk
from modules import shortcuts
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
        self.root.bind("<Prior>", lambda e: self.gui.teste(e))
        self.root.bind("<Configure>", lambda e: self.ajustar_resolucao(e))
        self.maintext.bind("<MouseWheel>", lambda _: "break")
        self.ok = 1


    def escape_deal(self):
        # if you're in a localdir Open file
        if self.main_app_instance.File.file_name == "__pytextLocaldir__":
            updir = self.main_app_instance.File.get_up_directory()
            self.main_app_instance.File.open_local_directory_or_file(updir, self.maintext, self.main_app_instance, self.gui, updir = True)
        
        else:
            self.trocar_modo(self.main_app_instance.modo)



    def ajustar_resolucao(self, *args):
        try:
            if int(self.root.winfo_height()) == int(self.lastheight):
                pass
            elif self.ok == 1:
                self.ok = 0
                self.root.update()
                print("mudança na resolução")
                self.gui.teste()
        except Exception:
            self.lastheight = self.root.winfo_height()



    def atualizar_contador_de_linhas_e_colunas_globais(self, *args):
        return self.gui.bottom_output_doc_info.configure(text=self.gui.obter_numero_de_linhas_e_colunas(f=True))


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
            
            # Caso não haja comandos e aperte :
            if comando == "":
                if tecla == "colon":
                    self.bottom_command_output.focus_set()


                elif tecla == "Return":
                    if self.main_app_instance.File.file_name == "__pytextLocaldir__":
                        posicao_linha_atual = self.gui.main_textarea.index(ctk.INSERT).split('.')[0]
                        conteudo_linha_atual = self.gui.main_textarea.get(f"{posicao_linha_atual}.0", f"{posicao_linha_atual}.end")
                        self.main_app_instance.File.open_local_directory_or_file(conteudo_linha_atual, self.maintext, self.main_app_instance, self.gui)
                    return
                
                else:
                    match tecla:
                        case "i":
                            if not self.main_app_instance.File.file_name == "__pytextLocaldir__":
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
            if numeros:
                return int(''.join(numeros))
            else:
                return 0

        comando_sem_numeros = re.sub(r'\d', '', comando)
        numeros = extrair_numeros(comando)

        # tratando o comando de fato
        command_output = shortcuts.search_command(comando_sem_numeros, numeros, self.maintext, self.main_app_instance, self.gui)

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
