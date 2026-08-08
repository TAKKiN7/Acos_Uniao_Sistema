import win32com.client
import pythoncom
from pathlib import Path
from tkinter import messagebox as msg
from time import sleep as pause


def baixar_anexos(chave):
    pythoncom.CoInitialize()
    try:
        numero = chave[27:34] if len(chave) >= 34 else chave

        pasta_usiminas = Path.home() / "Desktop" / "USIMINAS"
        xml_novo = pasta_usiminas / f"{chave}.xml"
        xml_antigo = pasta_usiminas / f"{chave} NF {numero}.xml"

        pause(1)

        if xml_novo.is_file() or xml_antigo.is_file():
            print('XML já existe no computador.')
        else:
            # Pasta onde os anexos serão salvos
            pasta_usiminas.mkdir(exist_ok=True)

            outlook = win32com.client.Dispatch("Outlook.Application")
            namespace = outlook.GetNamespace("MAPI")

            caixa_entrada = namespace.GetDefaultFolder(6)

            for email in caixa_entrada.Items:
                try:
                    assunto = str(getattr(email, "Subject", ""))
                    if numero in assunto:
                        print(f"E-mail encontrado: {assunto}")
                        attachments = getattr(email, "Attachments", None)
                        if attachments:
                            for i in range(1, attachments.Count + 1):
                                anexo = attachments.Item(i)
                                arquivo = Path(anexo.FileName)
                                
                                if arquivo.suffix.lower() == ".pdf":
                                    novo_nome = f"{chave} NF {numero}{arquivo.suffix}"
                                else:
                                    novo_nome = f"{chave}.xml"
                                    
                                caminho = pasta_usiminas / novo_nome
                                anexo.SaveAsFile(str(caminho))
                                print(f"Anexo salvo: {novo_nome}")
                except Exception as e_item:
                    print(f"Erro ao ler item de e-mail: {e_item}")

    except Exception as e:
        print(f"Erro ao baixar anexos USIMINAS: {e}")
        msg.showerror("Falha", f"Ocorreu um erro durante a busca do XML Usiminas:\n{e}")
    finally:
        pythoncom.CoUninitialize()