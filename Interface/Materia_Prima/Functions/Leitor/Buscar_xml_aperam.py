import win32com.client
from pathlib import Path
from tkinter import messagebox as msg




def baixar_anexos(chave):

    try:  
        numero = chave[27:34]


        # Pasta onde os anexos serão salvos

        destino = Path.home() / "Desktop" / "APERAM"

        destino.mkdir(exist_ok=True)

        outlook = win32com.client.Dispatch("Outlook.Application")
        namespace = outlook.GetNamespace("MAPI")

        caixa_entrada = namespace.GetDefaultFolder(6)

        for email in caixa_entrada.Items:

            assunto = str(email.Subject)

            if numero in assunto:

                print(f"E-mail encontrado: {assunto}")

                for i in range(1, email.Attachments.Count + 1):

                    anexo = email.Attachments.Item(i)

                    arquivo = Path(anexo.FileName)

                    novo_nome = f"{chave} NF {numero}{arquivo.suffix}"

                    caminho = destino / novo_nome

                    anexo.SaveAsFile(str(caminho))

                    print(f"Anexo salvo: {anexo.FileName}")
    except:
        msg.showerror("Falha", "Ocorreu um erro durante a leitura da chave de acesso, tente novamente por favor.")
    else:
        pass