import re
import customtkinter as ctk

def search_command(comando:str, qtd:int, textbox):
    comando = re.sub(r'[^a-zA-Z]', '', comando)

    match comando:

        case "dd":
            deletar_linha(qtd, textbox)
        
        case _:
            print("Comando não encontrado.")


def deletar_linha(final: int, textbox):
    inicio = f"{str(textbox.index(ctk.INSERT)).split('.')[0]}.0"
    final = str(final + float(inicio))

    textbox.configure(state="normal")
    textbox.delete(inicio, final)
    textbox.configure(state="disabled")
    return 0
