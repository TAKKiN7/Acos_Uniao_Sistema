import xml.etree.ElementTree as ET
from pathlib import Path





def leitura_xml(chave):
    ns = {'nfe': 'http://www.portalfiscal.inf.br/nfe'}
    
    numero = chave[27:34]

    # nota = filedialog.askopenfilename()
    nota = Path(Path.home() / "Desktop" / "GERDAU" / f"{chave} NF {numero}.xml")
    
    print(nota)

    tree = ET.parse(nota)
    root = tree.getroot()

    numero_nf = root.find('.//nfe:nNF', ns)

    if numero_nf is not None:
        #print(numero_nf.text)
        pass


    inf_cpl = root.find('.//nfe:infCpl', ns)

    #print(inf_cpl.text)

    index = inf_cpl.text.find("11411000")

    lote = inf_cpl.text[index + 8:index + 8 + 12]
    #print(lote)

    t_peso = root.find('.//nfe:pesoL', ns)
    
    if t_peso is not None:
        peso = t_peso.text[:-4]

    return [numero_nf.text, lote, peso]


if __name__ == "__main__":
    print(leitura_xml())