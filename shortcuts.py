import re
import customtkinter as ctk

def search_command(comando:str, qtd:int, textbox):
    comando = re.sub(r'[^a-zA-Z]', '', comando)

    match comando:

        case "dd":
            deletar_linha(qtd, textbox)
        
        case "w" | "a" | "s" | "d":
            mover_cursor(comando, qtd, textbox)
        
        case "Q":
            exit()

        case _:
            print("Comando não encontrado.")


# dd
def deletar_linha(final: int, textbox):
    inicio = f"{str(textbox.index(ctk.INSERT)).split('.')[0]}.0"

    if final == 1:
        final = str(final + float(inicio))

    else:
        final = str(final + float(inicio) + 1)

    textbox.configure(state="normal")
    textbox.delete(inicio, final)
    textbox.configure(state="disabled")
    return 0


# w
def mover_cursor(pos, qtd, textbox):
    linha_atual = int(textbox.index(ctk.INSERT).split(".")[0])
    coluna_atual = int(textbox.index(ctk.INSERT).split(".")[1])
    match pos:
        case "w":
            nova_posicao = max(linha_atual - qtd, 1)  # Garante que a posição não seja menor que 1
            nova_posicao = f"{nova_posicao}.{coluna_atual}"

        case "a":
            nova_posicao = max(coluna_atual - qtd, 0)
            nova_posicao = f"{linha_atual}.{nova_posicao}"

        case "s":
            nova_posicao = max(linha_atual + qtd, 1)
            nova_posicao = f"{nova_posicao}.{coluna_atual}"

        case "d":
            nova_posicao = max(coluna_atual + qtd, 0)
            nova_posicao = f"{linha_atual}.{nova_posicao}"

    textbox.mark_set(ctk.INSERT, nova_posicao)
    textbox.see(nova_posicao)

