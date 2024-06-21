import tkinter as tk

# Cria a janela principal
root = tk.Tk()

# Define o fundo da janela principal como preto
root.configure(bg='#2b2538')

# Cria um frame
frame = tk.Frame(root, bg='black')
# frame.pack(expand=True, fill='both')

# Adiciona widgets ao frame (exemplo)
label = tk.Label(frame, text="Texto branco no fundo preto", fg="white", bg="black")
label.pack(padx=20, pady=20)

# Inicia o loop principal
root.mainloop()
