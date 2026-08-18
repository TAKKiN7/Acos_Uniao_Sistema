from pyautogui import *
from time import sleep
from keyboard import wait, is_pressed
from pyperclip import copy
import mouse
from tkinter import messagebox as msg

from Interface.Materia_Prima.Functions.Leitor.Buscar_xml_gerdau import baixar_anexos
from Interface.Materia_Prima.Functions.Leitor.Leitor_Gerdau import leitura_xml







def pause(time=0.5):
    sleep(time)




def enter__(times=2, time=0):
    for c in  range(times):
        press("enter")
        sleep(time)


def wait_enter():
    while True:
        if mouse.is_pressed("x2") or mouse.is_pressed("middle"):
            return True  # Sai do loop quando Enter for pressionado
        elif mouse.is_pressed("x") or mouse.is_pressed("right"):
            return False
        sleep(0.1)  # Pequena pausa para não sobrecarregar o CP



def gerdau_start(chave, xml=True):

    


    if xml:
        baixar_anexos(chave)
        valores = leitura_xml(chave)
        nota = valores[0]
        lote = valores[1]
        peso = valores[-1]

        


    res = msg.askyesno("Confirme as informações", f"""Número da Nota: {nota}
Numeração do Lote: {lote}
Peso: {peso}""")

    if not res:
        return

    res = wait_enter()
    if not res:
        return

    

    operador = "eustaquio"
    senha = "eustaqui"



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
    write("916")
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
    for l in peso:
        write(l)
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
    
    for l in lote:
        write(l)

    enter__(1)
    for p in peso:
        write(p)


    enter__(2)
    write("1")
    enter__(1)
    write("916")
    res = wait_enter()
    if not res:
        return
    enter__(6)
    pause(1)

    press("tab")

    res = wait_enter()
    if not res:
        return
    
    pause(0.5)
    enter__(4, 1)

    moveTo(x=723, y=561)
    
    res = wait_enter()
    if not res:
        return
    
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
    
    enter__()
    pause(1.5)
    
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
    for n in lote:
        write(n)
    
    enter__(3)
    pause()
    click(x=971, y=674)
    pause()

    print("confirme a classificação")
    res = wait_enter()
    if not res:
        return
    write(operador)
    press("tab")
    write(senha)
    press("tab")
    press("enter")

    pause()

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
    gerdau_start()

    