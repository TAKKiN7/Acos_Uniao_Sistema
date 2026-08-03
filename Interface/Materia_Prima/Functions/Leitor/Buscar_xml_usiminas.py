import win32com.client
from pathlib import Path
from tkinter import messagebox as msg
from time import sleep as pause



def baixar_anexos(chave):

    try:  
        numero = chave[27:34]


        xml = Path(Path.home() / "Desktop" / "USIMINAS" / f"{chave} NF {numero}.xml")
        pause(1)


        print(xml)

        if xml.is_file():
            print('to aqui')
        
       
        else:
            # Pasta onde os anexos serão salvos
            destino = Path.home() / "Desktop" / "USIMINAS"
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
    except Exception as e:

        print(f"Erro: {e}")
        msg.showerror(
        "Falha",
        f"Ocorreu um erro:\n{e}"
        )
        #msg.showerror("Falha", "Ocorreu um erro durante a leitura da chave de acesso, tente novamente por favor.")
    else:
        pass