from pyautogui import *
from time import sleep, time
from keyboard import wait, is_pressed
import mouse
from tkinter import messagebox as msg






def pause(time=0.3):
    sleep(time)




def enter__(times=2, time=0):
    for c in  range(times):
        press("enter")
        sleep(time)


def wait_enter():
    while True:
        if mouse.is_pressed("x2"):
            return True
        elif mouse.is_pressed("x"):
            return False
        sleep(0.1)


def aperam_start(chave : str, lotes : str):
    print("Pronto para começar?")
    

    nota = chave[27:34]

    res = msg.askyesno("Confirme", f"""Número da Nota: {nota}
Lotes: {lotes}""")
    if not res:
        return
    
    res = wait_enter()
    if not res:
        return


    #print("Conferiu o número de lote e foi pra aba do faturamento?")
    #wait_enter()
    click(x=33, y=71)
    pause(0.5)
    click(x=126, y=129)
    pause(1.5)
    click(x=14, y=31)
    pause()
    moveTo(x=103, y=274)
    pause(0.7)
    moveTo(x=366, y=315)
    pause()
    click(x=366, y=315)

    res = wait_enter()
    if not res:
        return


    doubleClick(x=354, y=330)
    press("enter")
    pause()
    click(x=606, y=364)
    enter__()
    pause()
    write("1831")
    pause()
    click(x=257, y=693)
    pause()
    enter__()

    res = wait_enter()
    if not res:
         return



    press("space")
    for n in nota:
        write(n)
    
    enter__()
    pause()
    enter__(1)
    moveTo(x=671, y=505)

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
    res = wait_enter()
    if not res:
        return

    for c in range(lotes):
        click(x=328, y=415)
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
        enter__(2)
        write("1")
        enter__(1)
        write("1831")
        enter__(6)
        pause(1)

    press("tab")
    res = wait_enter()
    if not res:
        return
    enter__(4, 1)
    
    res = wait_enter()
    if not res:
        return
    
    enter__(6)

    write("NFe")
    enter__(3)
    write("301")
    enter__(1)
    write("3505")


    res = wait_enter()
    if not res:
        return
    click(x=40, y=75)
    pause(.5)
    click(x=153, y=380)
    pause(1)
    click(x=83, y=31)
    click(x=93, y=54)
    pause()
    click(x=518, y=79)
    pause()
    click(x=640, y=395)
    enter__()
    pause()
    click(x=796, y=480)
    pause()
    moveTo(x=1334, y=157)
    pause()
    dragTo(1332, 605, duration=0.5, button="left")


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
    # numero_nota = str(input("Digite o número da nota: "))
    # lotes = str(input("Quantidade de lotes: "))
    
    # aperam_start(numero_nota, lotes)
    print("confirme a classificação")
    def aqui():
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

    aqui()