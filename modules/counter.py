import customtkinter as ctk

class Counter:
    def __init__(self, main_app_instance):
        self.main_app_instance = main_app_instance
        self.root = main_app_instance.root
        self.Font = main_app_instance.Font
        self.old_linha_visivel = 0
        self.labels = []
    
    
    def create_counter(self, *args):
        # Sem o update ele nao consegue calcular o num de linhas
        self.root.update()
        self.root.update_idletasks()


        # Define um valor super alto para que depois ele defina o certinho na resolução
        self.gui.main_textarea._textbox.configure(height=9999)

        self.max_linhas_visiveis = self.calcular_numero_de_linhas_visiveis()
        self.distancias = [i for i in range(self.max_linhas_visiveis)]

        # Definindo o valor certinho agora. Precisa disso para nao ter problemas no tamanho da caixa de texto
        self.gui.main_textarea._textbox.configure(height=self.max_linhas_visiveis)
    

    def calcular_numero_de_linhas_visiveis(self):
            self.gui.main_textarea.update_idletasks()  # Atualiza a geometria antes de calcular
            self.gui.main_textarea.update()

            try:
                height = self.gui.main_textarea.winfo_height()
                # antigo e problematico abaixo
                #line_height = self.gui.main_textarea.dlineinfo("1.0")[3]  # Altura da primeira linha
                line_height = self.Font.size  # Altura da primeira linha
                visible_lines = height // line_height
                #print("num de linhas calculado")
                return visible_lines

            # provavelmente esse except é inutil agora que estou acessando o tamanho da fonte pela classe ali em cima
            except TypeError as err:
                print("nao consegui contar: ", err)
                # cuidar aqui, isso pode nao funcionar. Fazer testes para encontrar a fonte desse erro
                self.root.configure(height=int(self.root.winfo_height()) - self.Font.size)
                return self.max_linhas_visiveis


    def create_labels(self):
        for label in self.labels:
            label.destroy()

        # resetando o array
        self.labels = []


        for i in range(0, self.max_linhas_visiveis):
            if i == 0:
                label = ctk.CTkLabel(self.gui.leftframe, text=str(i), font=self.Font.font)
                label.grid(row=i, column=0, sticky="en", pady=(28.75,0))
            else:
                label = ctk.CTkLabel(self.gui.leftframe, text=str(i), font=self.Font.font)
                label.grid(row=i, column=0, sticky="en", pady=(0))

            self.labels.append(label)


    def get_visible_line(self, text_widget):
        # Obtém a informação da linha atual
        cursor_pos = text_widget.index(ctk.INSERT)
        line_number = int(cursor_pos.split('.')[0])
        
        # Calcula a primeira linha visível na tela
        first_visible_line = int(text_widget.index("@0,0").split('.')[0])
        
        # Calcula a linha visível atual
        visible_line = line_number - first_visible_line + 1
        
        return visible_line



    def atualizar_contador(self, *args):
        #self.count_visible_lines()
        self.label_value = self.get_visible_line(self.gui.main_textarea) - 1

        # preciso encontrar uma forma de retornar o numero de caracteres que o texto de acordo com a resolução suporta
        # ou então comparar e ver se as linhas visiveis são a mesma linha absoluta

        posicao_atual = self.gui.main_textarea.index(ctk.INSERT)
        numero_linha_atual = int(posicao_atual.split('.')[0])
        
        # definindo o texto da linha atual
        #self.labels[self.label_value - 1].configure(text=numero_linha_atual)
        
        self.calcular_distancias(self.labels, self.label_value)

        actual_visible_line = int(self.gui.main_textarea.index(ctk.INSERT).split('.')[0])

        #print(self.gui.main_textarea.dlineinfo(self.gui.main_textarea.index(ctk.INSERT)))

        for label in self.labels:
            cur_row = label.grid_info()["row"]
            
            #print("cur_row: ", cur_row, " actual_line: ", actual_visible_line)
            #if cur_row == actual_visible_line:
            #    print("sao iguais")
            




    def calcular_distancias(self, array, posicao_zero):
        # Calcular a distância entre cada elemento e o elemento 0
        self.distancias = [abs(i - posicao_zero) for i in range(len(array))]
        
        for i, valor in enumerate(self.distancias):
            if valor == 0:
                self.distancias[i] = int(self.gui.main_textarea.index(ctk.INSERT).split(".")[0])
            
            self.labels[i].configure(text=self.distancias[i])

        self.p()  
        #for i in self.tes():
        #    self.labels[i].configure(text="")

        return 


    def p(self):
        # both first n last in relative number (0 to 21 for example), (1, 22), (2, 23), (3, 24), ... (10, 31)
        first_visible_line = int(self.gui.main_textarea.index("@0,0").split('.')[0])
        last_visible_line = int(self.gui.main_textarea.index(f"@0,{self.Font.size * (self.max_linhas_visiveis)}").split('.')[0])

        # getting all content in visible lines to iterate per line
        linhas_visiveis = self.gui.main_textarea.get(f"{first_visible_line}.0"+" linestart", f"{last_visible_line}.0"+" lineend")

        print("-------------------------------------")
        # ele pode estar chamando o isWrapped em uma linha invisivel
        for i in range(first_visible_line, last_visible_line + 1):
            # print(i - first_visible_line) # i - first_visible_line is 0
            print(self.gui.main_textarea.isWrapped(i))
            pass
        #for i, linha in enumerate(linhas_visiveis.split("\n")):
            # printa o index das linhas visiveis
            #print(i, linha)
            #print


    def tes(self):
        linhas_grandes = []
        first_visible_line = int(self.gui.main_textarea.index("@0,0").split('.')[0])
        # pegando a ultima linha visivel com tamanho em px da fonte * max de linhas visiveis
        
        print("FVL: ", first_visible_line)
        # o TypeError tá aqui nessa linha   
        last_visible_line = int(self.gui.main_textarea.index(f"@0,{self.Font.size * (self.max_linhas_visiveis)}").split('.')[0])
        linhas_visiveis = self.gui.main_textarea.get(f"{first_visible_line}.0"+" linestart", f"{last_visible_line}.0"+" lineend")
        for i, linha in enumerate(linhas_visiveis.split("\n")):

            cursor_pos = i + 1
            print(f"se {cursor_pos} - {first_visible_line} entre {first_visible_line} e {last_visible_line}")

            if last_visible_line >= cursor_pos - first_visible_line >= first_visible_line:
                print(f"{cursor_pos} é visivel")
            else:
                print(f"{cursor_pos} não é visivel")
            # i é a posição das linhas visiveis, se eu mandar pra absolutas pode funcionar
            # a função isWrapped() dá erro se vc usar uma linha absoulta que não está visível
            
            #if self.check_if_line_is_visible(i - first_visible_line):
                #print(linha, ": ", self.gui.main_textarea.isWrapped(i + first_visible_line + 1))
                #print(linha, "eh visivel")
            """
            # precisa encontrar o numero de colunas que o texto aguenta aqui e trocar pelo 94
            if len(linha) // 94 >= 1:
                #print(i, " eh grande")

                for x in range(0, len(linha) // 94):
                    linhas_grandes.append(i + x + 1 + len(linhas_grandes))"""
        
        return linhas_grandes
    
    def check_if_line_is_visible(self, line_to_check: int):
        first_visible_line = int(self.gui.main_textarea.index("@0,0").split('.')[0])
        last_visible_line = int(self.gui.main_textarea.index(f"@0,{self.Font.size * (self.max_linhas_visiveis)}").split('.')[0])
        line_to_check += 1

        print("----------------------------")
        for i in range(first_visible_line, last_visible_line + 1):
            print(f"se {i} + {first_visible_line} == {line_to_check}")

            #return i + first_visible_line == line_to_check


    def count_visible_lines(self):
        first_visible_line = int(self.gui.main_textarea.index("@0,0").split('.')[0])
        last_visible_line = int(self.gui.main_textarea.index(f"@0,{self.Font.size * self.max_linhas_visiveis}").split('.')[0])


        linha_visivel_atual = self.get_visible_line(self.gui.main_textarea)

        conteudo_linha = self.gui.main_textarea.get(f"{linha_visivel_atual}.0"+" linestart", f"{linha_visivel_atual}.0"+" lineend")

        #print("LInha visivel atual: ",linha_visivel_atual, "old: ", self.old_linha_visivel)

        #if linha_visivel_atual == self.old_linha_visivel:
            #print("essa linha ocupa mais espaços")

        self.old_linha_visivel = linha_visivel_atual
