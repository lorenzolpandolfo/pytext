import re
import customtkinter as ctk
import os

def search_command(comando:str, qtd:int, textbox, mainapp):
    # Se o qtd não for indicado, vai ser entendido como 0
    # limitando à apenas caracteres de texto
    comando = re.sub(r'[^a-zA-Z]', '', comando)

    match comando:

        case "dd":
            print(qtd)
            return deletar_linha(qtd, textbox)
        
        case "w" | "a" | "s" | "d":
            return mover_cursor(comando, qtd, textbox)
        
        case "Q":
            return "sair"
        
        case "S":
            return save(textbox, mainapp)
        
        case "SQ" | "QS" | "WQ" | "wq":
            if save(textbox, mainapp):
                return "sair"

        case _:
            return "Comando não encontrado."


# dd   - delete lines
def deletar_linha(final: int, textbox):
    inicio = f"{str(textbox.index(ctk.INSERT)).split('.')[0]}.0"
    
    final = str(final + float(inicio) + 1)

    textbox.configure(state="normal")
    textbox.delete(inicio, final)
    textbox.configure(state="disabled")

    final = final.replace(".0", "")
    inicio = inicio.replace(".0", "")

    final = int(final) - int(inicio) - 1
    return f"{final} linhas apagadas".replace("0", "1")


# wasd - move through lines
def mover_cursor(pos, qtd, textbox):
    # caso vc apenas insira o comando de movimento, sem qtd
    if qtd == 0:
        qtd = 1
    
    linha_atual = int(textbox.index(ctk.INSERT).split(".")[0])
    coluna_atual = int(textbox.index(ctk.INSERT).split(".")[1])
    detail_output = ""

    match pos:
        case "w":
            nova_posicao = max(linha_atual - qtd, 1)  # Garante que a posição não seja menor que 1
            nova_posicao = f"{nova_posicao}.{coluna_atual}"
            detail_output = f"Cursor movido {qtd} linhas acima"

        case "a":
            nova_posicao = max(coluna_atual - qtd, 0)
            nova_posicao = f"{linha_atual}.{nova_posicao}"
            detail_output = f"Cursor movido {qtd} colunas à esquerda"

        case "s":
            nova_posicao = max(linha_atual + qtd, 1)
            nova_posicao = f"{nova_posicao}.{coluna_atual}"
            detail_output = f"Cursor movido {qtd} linhas abaixo"

        case "d":
            nova_posicao = max(coluna_atual + qtd, 0)
            nova_posicao = f"{linha_atual}.{nova_posicao}"
            detail_output = f"Cursor movido {qtd} colunas à direita"

    textbox.mark_set(ctk.INSERT, nova_posicao)
    textbox.see(nova_posicao)
    return detail_output


# S    - save the current file to a directory
def save(textbox, mainapp):
    content = textbox.get("1.0", ctk.END)
    
    if mainapp.file_name:
        full_path = os.path.join(mainapp.File.terminal_directory, mainapp.File.file_name)

        with open(full_path, "w", encoding="utf8") as new_file:
            new_file.write(content)
            return f"{mainapp.File.file_name} salvo"

    else: return False