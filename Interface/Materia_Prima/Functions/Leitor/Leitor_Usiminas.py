import sys
import xml.etree.ElementTree as ET
from pathlib import Path
 
# --- Constantes (DRY) -------------------------------------------------------
NFE_NS = {"nfe": "http://www.portalfiscal.inf.br/nfe"}
XPATH_VOLUMES = ".//nfe:transp/nfe:vol"
XPATH_NNF = ".//nfe:ide/nfe:nNF"
 
TAG_LOTE = "nfe:nVol"
TAG_PESO_LIQ = "nfe:pesoL"
TAG_PESO_BRUTO = "nfe:pesoB"
TAG_PECAS = "nfe:qVol"
 
TITULO_JANELA = "Selecione o(s) XML da NF-e"
FILTRO_ARQUIVOS = [("Arquivos XML", "*.xml"), ("Todos os arquivos", "*.*")]
 
 
def carregar_xml(caminho_xml: str) -> ET.Element:
    """Faz o load do XML e retorna o elemento raiz da NF-e."""
    arvore = ET.parse(caminho_xml)
    return arvore.getroot()
 
 
def selecionar_arquivos() -> tuple[str, ...]:
    """Abre uma janela do Windows para o usuario escolher um ou mais XMLs."""
    # Import local: tkinter e nativo do Python no Windows, mas so e carregado
    # se o script for executado sem argumentos (evita erro em servidores sem GUI)
    from tkinter import Tk
    from tkinter.filedialog import askopenfilenames
 

    janela = Tk()
    janela.withdraw()          # esconde a janela principal vazia do Tk
    janela.attributes("-topmost", True)  # garante que o dialogo abra na frente
    caminhos = askopenfilenames(title=TITULO_JANELA, filetypes=FILTRO_ARQUIVOS)
    janela.destroy()
    return caminhos
 
 
def _texto(elemento: ET.Element, tag: str) -> str | None:
    """Retorna o texto de uma sub-tag, ou None se ela nao existir."""
    filho = elemento.find(tag, NFE_NS)
    return filho.text if filho is not None else None
 
 
def extrair_volumes(raiz: ET.Element) -> list[dict]:
    """Recebe a raiz da NF-e e retorna uma lista de dicts, um por volume (lote)."""
    volumes = []
    for indice, vol in enumerate(raiz.findall(XPATH_VOLUMES, NFE_NS), start=1):
        volumes.append(
            {
                "item": indice,  # ordem em que aparece no XML
                "lote": _texto(vol, TAG_LOTE),
                "peso_liquido": float(_texto(vol, TAG_PESO_LIQ) or 0),
                "peso_bruto": float(_texto(vol, TAG_PESO_BRUTO) or 0),
                "pecas": int(_texto(vol, TAG_PECAS) or 0),
            }
        )
    return volumes
 
 
def processar_nfe(caminho_xml: str) -> None:
    """Carrega um XML, extrai os volumes e imprime o resultado."""
    raiz = carregar_xml(caminho_xml)
 
    numero_nf = raiz.find(XPATH_NNF, NFE_NS)
    #print(f"\nArquivo: {caminho_xml}")
    #print(f"NF-e numero: {numero_nf.text if numero_nf is not None else '?'}")
 
    volumes = extrair_volumes(raiz)
    #"print(f"Volumes encontrados: {len(volumes)}")
    
    volumes.insert(0, numero_nf.text)

    return volumes

 
def leitura_xml(chave):

    caminho_pasta  : Path = Path.home() / r"Desktop\USIMINAS"
    numero = chave[27:34]



    caminho = rf"{caminho_pasta}\{chave} NF {numero}.xml"
 

    volumes = processar_nfe(caminho)


    
    return volumes


 
if __name__ == "__main__":
    leitura_xml()