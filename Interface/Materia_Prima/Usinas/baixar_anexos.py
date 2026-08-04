import win32com.client
import pythoncom
from pathlib import Path
from tkinter import messagebox as msg


def baixar_anexos(chave):
    pythoncom.CoInitialize()
    try:
        numero = chave[27:34] if len(chave) >= 34 else chave

        # Pasta onde os anexos serão salvos
        destino_xml = Path.home() / "Desktop" / "XML"
        destino_xml.mkdir(exist_ok=True)

        destino_certificado = Path.home() / "Desktop" / "CERTIFICADOS"
        destino_certificado.mkdir(exist_ok=True)

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
                            novo_nome = f"{arquivo.stem} NF {numero}{arquivo.suffix}"

                            if arquivo.suffix.lower() == ".pdf":
                                caminho = destino_certificado / novo_nome
                            else:
                                caminho = destino_xml / novo_nome

                            anexo.SaveAsFile(str(caminho))
                            print(f"Anexo salvo: {anexo.FileName}")
            except Exception as e_item:
                print(f"Erro ao processar item do Outlook: {e_item}")

    except Exception as e:
        msg.showerror("Falha", f"Ocorreu um erro durante a leitura da chave de acesso:\n{e}")
    finally:
        pythoncom.CoUninitialize()


def baixar_xml(chave):
    pythoncom.CoInitialize()
    try:
        numero = chave[27:34] if len(chave) >= 34 else chave

        # Pasta onde os anexos serão salvos
        destino_xml = Path.home() / "Desktop" / "XML"
        destino_xml.mkdir(exist_ok=True)

        destino_certificado = Path.home() / "Desktop" / "CERTIFICADOS"
        destino_certificado.mkdir(exist_ok=True)

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
                            novo_nome = f"{chave} NF {numero}{arquivo.suffix}"

                            if arquivo.suffix.lower() == ".pdf":
                                continue
                            else:
                                caminho = destino_xml / novo_nome

                            anexo.SaveAsFile(str(caminho))
                            print(f"Anexo salvo: {anexo.FileName}")
            except Exception as e_item:
                print(f"Erro ao processar item do Outlook: {e_item}")

    except Exception as e:
        msg.showerror("Falha", f"Ocorreu um erro durante a leitura da chave de acesso:\n{e}")
    finally:
        pythoncom.CoUninitialize()