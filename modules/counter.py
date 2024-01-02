import customtkinter as ctk

class Counter:
    def __init__(self, main_app_instance):
        self.main_app_instance = main_app_instance
        self.root = main_app_instance.root
        self.Font = main_app_instance.Font
        self.labels = []
    
    
    def create_counter(self, *args):
        # Sem o update ele nao consegue calcular o num de linhas
        self.root.update()
        self.root.update_idletasks()

        # Define um valor super alto para que depois ele defina o certinho na resolução
        self.gui.main_textarea._textbox.configure(height=9999)

        self.max_linhas_visiveis = self.calcular_numero_de_linhas_visiveis()

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
        num = self.max_linhas_visiveis

        for label in self.labels:
            label.destroy()

        # resetando o array
        self.labels = []


        for i in range(0, num):
            if i == 0:
                label = ctk.CTkLabel(self.gui.leftframe, text=str(i), font=self.Font.font)
                label.grid(row=i, column=0, sticky="en", pady=(28.75,0))
            else:
                label = ctk.CTkLabel(self.gui.leftframe, text=str(i), font=self.Font.font)
                label.grid(row=i, column=0, sticky="en", pady=(0))

            #label.rowconfigure(i,weight=1)
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
        self.label_value = self.get_visible_line(self.gui.main_textarea) - 1

        posicao_atual = self.gui.main_textarea.index(ctk.INSERT)
        numero_linha_atual = int(posicao_atual.split('.')[0])
        
        # definindo o texto da linha atual
        self.labels[self.label_value - 1].configure(text=numero_linha_atual)
        
        self.calcular_distancias(self.labels, self.label_value)


    def calcular_distancias(self, array, posicao_zero):
        # Calcular a distância entre cada elemento e o elemento 0
        distancias = [abs(i - posicao_zero) for i in range(len(array))]
        
        for i, valor in enumerate(distancias):
            if valor == 0:
                distancias[i] = int(self.gui.main_textarea.index(ctk.INSERT).split(".")[0])     
            
            self.labels[i].configure(text=distancias[i])

        
        return distancias