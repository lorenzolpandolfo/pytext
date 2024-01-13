import re
import customtkinter as ctk
import os

def search_command(comando:str, qtd:int, textbox, mainapp, gui):
    # Se o qtd não for indicado, vai ser entendido como 0
    # limitando à apenas caracteres de texto
    comando = re.sub(r'[^a-zA-Z]', '', comando)

    match comando:
        case "dd":
            return deletar_linha(qtd, textbox)
        
        case "w" | "a" | "s" | "d":
            return mover_cursor(comando, qtd, textbox)
        
        case "Q":
            return "sair"
        
        case "S":
            return save(textbox, mainapp, gui)
        
        case "SQ" | "QS" | "WQ" | "wq":
            if save(textbox, mainapp, gui):
                return "sair"
        
        case "O":
            return mainapp.File.load_local_files_to_open(textbox, mainapp)
        
        case "nf":
            return mainapp.File.create_new_file(gui)

        case "nd":
            mainapp.File.insert_new_dir_title(gui)

        case _:
            return "Command not found"





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
            detail_output = f"Cursor moved {qtd} lines above"

        case "a":
            nova_posicao = max(coluna_atual - qtd, 0)
            nova_posicao = f"{linha_atual}.{nova_posicao}"
            detail_output = f"Cursor moved {qtd} columns left"

        case "s":
            nova_posicao = max(linha_atual + qtd, 1)
            nova_posicao = f"{nova_posicao}.{coluna_atual}"
            detail_output = f"Cursor moved {qtd} lines below"

        case "d":
            nova_posicao = max(coluna_atual + qtd, 0)
            nova_posicao = f"{linha_atual}.{nova_posicao}"
            detail_output = f"Cursor moved {qtd} columms right"

    textbox.mark_set(ctk.INSERT, nova_posicao)
    textbox.see(nova_posicao)
    return detail_output


# S    - save the current file to a directory
def save(textbox, mainapp, gui):
    
    if mainapp.File.file_name != "":
        print("FILE NAME: ", mainapp.File.file_name)
        # In this case, you're saving the SavePreset file
        if mainapp.File.file_name == "__pytextSavePreset__":
            mainapp.File.file_name = textbox.get("1.0", "1.end")
            content = gui.buffer_content
        
        # Creating a new dir title
        elif mainapp.File.file_name == "__pytextNewDirTitle__":
            dir_name = textbox.get("1.0", "1.end")
            return mainapp.File.create_new_directory(dir_name, textbox, mainapp)


            
        else:
            # Get all the content in this current file
            content = textbox.get("1.0", ctk.END)
            gui.buffer_content = content

        full_path = os.path.join(mainapp.File.terminal_directory, mainapp.File.file_name)

        with open(full_path, "w", encoding="utf8") as new_file:
            new_file.write(content)

            # check if you just added a title to a non-title file
            if mainapp.File.file_name == textbox.get("1.0", "1.end"):
                # Loading the old file 
                gui.write_another_file_content(gui.buffer_content, file_name=textbox.get("1.0", "1.end"))

            return f"{mainapp.File.file_name} saved"

    # this runs when you save a file that doesn't have a title yet
    else:
        # Saving the current file content so you can edit the SavePreset file
        gui.buffer_content = textbox.get("1.0", ctk.END)
        
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        os.chdir("..")
        savepreset = os.path.join(os.getcwd(), ".temp", "__pytextSavePreset__.txt")

        with open(savepreset, "r", encoding="utf8") as savepresetfile:
            content = savepresetfile.read()
            gui.write_another_file_content(content, "", True)
        
        mainapp.File.file_name = "__pytextSavePreset__"