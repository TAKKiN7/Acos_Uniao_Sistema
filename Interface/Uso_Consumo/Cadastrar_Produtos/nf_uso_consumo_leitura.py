import xml.etree.ElementTree as ET
from pathlib import Path

def ler_nfe(chave: str) -> dict:
    chave = chave.strip()
    caminho_xml: Path = Path.home() / f"Desktop/Notas Consumo/{chave}.xml"

    if not caminho_xml.exists():
        raise FileNotFoundError(f"Arquivo XML não encontrado em:\n{caminho_xml}")

    ns = {"nfe": "http://www.portalfiscal.inf.br/nfe"}

    tree = ET.parse(caminho_xml)
    root = tree.getroot()

    emit = root.find(".//nfe:emit", ns)
    ide = root.find(".//nfe:ide", ns)

    dados = {
        "emitente": emit.findtext("nfe:xNome", default="", namespaces=ns) if emit is not None else "",
        "numero_nf": ide.findtext("nfe:nNF", default="", namespaces=ns) if ide is not None else "",
        "itens": []
    }

    for det in root.findall(".//nfe:det", ns):
        prod = det.find("nfe:prod", ns)
        if prod is not None:
            item = {
                "codigo": prod.findtext("nfe:cProd", default="", namespaces=ns),
                "descricao": prod.findtext("nfe:xProd", default="", namespaces=ns),
                "ncm_sh": prod.findtext("nfe:NCM", default="", namespaces=ns),
                "unidade": prod.findtext("nfe:uCom", default="", namespaces=ns),
                "quantidade": float(prod.findtext("nfe:qCom", default="0", namespaces=ns)),
                "valor_unitario": float(prod.findtext("nfe:vUnCom", default="0", namespaces=ns)),
            }
            dados["itens"].append(item)

    return dados
