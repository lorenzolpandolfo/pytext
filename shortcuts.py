import re
import customtkinter as ctk

def search_command(comando:str, qtd:int, textbox):
    comando = re.sub(r'[^a-zA-Z]', '', comando)

    match comando:

        case "dd":
            deletar_linha(f"{str(qtd + 1)}.0", textbox)
        
        case _:
            print("Comando não encontrado.")


def deletar_linha(final: str, textbox):
    textbox.configure(state="normal")
    print("FINAL: ", final)
    textbox.delete("1.0", final)
    textbox.configure(state="disabled")
    return 0
