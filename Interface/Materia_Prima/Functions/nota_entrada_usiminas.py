from pyautogui import *
from time import sleep
import mouse
from Interface.Materia_Prima.Functions.Leitor.Leitor_Usiminas import leitura_xml
from Interface.Materia_Prima.Functions.Leitor.Buscar_xml_usiminas import baixar_anexos
from tkinter import messagebox as msg




def pause(time=0.5):
    sleep(time)




def enter__(times=2, time=0):
    for c in  range(times):
        press("enter")
        sleep(time)


def wait_enter():
    while True:
        if mouse.is_pressed("x2"):
            return True  # Sai do loop quando Enter for pressionado
        elif mouse.is_pressed("x"):
            return False
        elif mouse.is_pressed("middle"):
            return "Titulo"
        sleep(0.1)  # Pequena pausa para não sobrecarregar o CP



def usiminas_start(chave):

    baixar_anexos(chave)
    res = leitura_xml(chave)

    nota = res[0]
    print("nota: ", nota)

    volumes = res[1:]

    print("volumes")
    print(volumes)

    peso = 0
    for v in volumes:
        peso += int(v.get("peso_liquido"))

    print(peso)

    info = ""
    for lote in volumes:
        info += f"Lote: {lote.get("lote")} - Peso Líquido: {int(lote.get("peso_liquido"))}\n"


    print(info)

    # if not volumes:
    #     return

    res = msg.askyesno("Confirme as informações", info)

    if not res:
        return

    
    


    clicks_tk = {
    "x" : [14, 65, 341, 530, 103, 366],
    "y" : [31, 252, 258, 293, 274, 315]
}


    x = clicks_tk.get("x")
    y = clicks_tk.get("y")

    operador = "eustaquio"
    senha = "eustaqui"

    
    
    res = wait_enter()
    if not res:
        return
    click(x=33, y=71)
    pause(0.5)
    click(x=126, y=129)
    pause(2)
    
    click(x=x[0], y=y[0]) # diária
    pause()
    click(x=x[1], y=y[1]) # compras
    pause()
    click(x=x[2], y=y[2]) # cadastro
    pause()
    click(x=x[3], y=y[3]) # XML
    pause(2)
    write("1854") # USINA
    click(x=792, y=523)  # OK
    pause()

    press("space")
    pause()
    for n in nota:
        write(n)
    enter__()
    pause(1)
    enter__(1)

    res = wait_enter()
    if not res:
        return

    for c in range(4):
        press("esc")

    press("F5") # BUSCA DE MODULOS
    write("MTM216")
    enter__()


    res = wait_enter()
    if not res:
        return
    
    
    doubleClick(x=354, y=330)
    press("enter")
    pause()
    click(x=606, y=364)
    enter__()
    pause()
    write("1854")
    pause()
    click(x=257, y=693)
    pause()
    enter__()  


    res = wait_enter()
    if not res:
         return

    press("space")
    pause()
    for n in nota:
        write(n)
    enter__()
    pause(1)
    enter__(1)

    moveTo(x=697, y=500)

    res = wait_enter()
    if not res:
        return
    
    click(x=1182, y=653)
    pause()
    click(x=1111, y=100)
    write("0")
    enter__(3)
    pause()
    click(x=982, y=694)
    pause()
    click(x=282, y=658)
    pause()
    click(x=739, y=228)
    pause(.5)

    pesoS = str(peso)
    
    for l in pesoS:
        write(l)


    print(pesoS)
    enter__(1)

    moveTo(x=909, y=580)

    res = wait_enter()
    if not res:
        return
    click(x=909, y=580)

    res = wait_enter()
    if not res:
        return
    pause()

    
    click(x=328, y=426)
    write("0")
    enter__(9)
    write("1,65")
    enter__(1)
    write("7,6")
    enter__(1)
    write("2")
    enter__(5)
    click(x=997, y=706)
    pause(1)
    enter__(1)
    res = wait_enter()
    if not res:
        return
    
    for lote in volumes:
        
        pesoS = str(int(lote.get("peso_liquido")))

        for l in lote.get("lote"):
            write(l)

        enter__(2)
        for p in pesoS:
            if p == ".":
                break
            write(p)


        enter__(2)
        write("1")
        enter__(1)
        write("1854")
        res = wait_enter()
        if not res:
            return
        enter__(6)
        pause(1)

        if lote != volumes[-1]:
            enter__(1)


    press("tab")

    res = wait_enter()
    if not res:
        return
    
    pause(0.5)
    enter__(4, 1)

    moveTo(x=723, y=561)
    
    res = wait_enter()
    if res == "Titulo":
        print("Nessa caso a nota possui titulo antecipado, certo?")
        pause(1)
    elif not res:
        return
    else:
        enter__(6)

        write("NFe")
        enter__(3)
        write("301")
        enter__(1)
        write("3505")
        press("tab")

    

    res = wait_enter()
    if not res:
        return

    
    for c in range(4):
        press("esc")

    press("F5") # BUSCA DE MODULOS
    write("GPM216")
    enter__()
    pause(.5)
    click(x=640, y=395)
    enter__()
    pause(.4)
    click(x=796, y=480)
    pause(.4)
    moveTo(x=1334, y=157)
    pause(1.5)

    click(x=610, y=199)
    press("space")

    lote = volumes[0].get("lote")

    for n in lote:
        write(n)
    
    enter__(3)
    pause()
    click(x=971, y=674)

    print("confirme a classificação")
    res = wait_enter()
    if not res:
        return
    write("eustaquio")
    press("tab")
    write("eustaqui")
    press("tab")
    press("enter")

    pause(1)

    num = "15"
    for  n in num:
        write(n)
    enter__()

    res = wait_enter()
    if not res:
        return
    write(".")
    press("tab")
    enter__(2)

    pause(1)
    for c in range(4):
        press("esc")




if __name__ == "__main__":

    usiminas_start()