from pyautogui import *
from time import sleep, time
from keyboard import wait, is_pressed
import mouse
from tkinter import messagebox as msg





def pause(time=0.2):
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


def esc():
    for c in range(5):
        press("esc")



def iniciar():
    res = wait_enter()
    if not res:
        return
     
    press("f5")

    write("mtm194")
    enter__()
    pause(.5)



    res = wait_enter()
    if not res:
        return
    click(x=715, y=357) # transportadora
    #moveTo(x=1097, y=682) # gravar

    res = wait_enter()
    if not res:
        return

    venda_especial : bool = msg.askyesno("Dúvida", "A venda é especial?")
    print(venda_especial)

    res = wait_enter()
    if not res:
        return
    click(x=1097, y=682) # gravar

    enter__()

    pause(.6)
    click(x=511, y=409) # desmarca ordem de expedicao
    pause(.4)
    click(x=510, y=333) # marca pedido de venda
    pause()
    click(x=820, y=525)   # clica em OK

    pause(.4)
    click(x=479, y=478) # imprimir

    res = wait_enter()
    if not res:
        return

    esc()


    press("F5")

    write("mtm724")
    enter__()

    res = wait_enter()
    if not res:
        return
    enter__()

    res = wait_enter()
    if not res:
        return
    enter__()

    pause(.5)
    click(x=239, y=293)

    moveTo(x=1025, y=678) # BOTAO PROSSEGUIR


    res = wait_enter()
    if not res:
        return

    esc()
    
    press("F5")

    write("mtm237")
    enter__()

    res = wait_enter()
    if not res:
        return

    write("eustaquio")
    enter__(1)
    write("eustaqui")
    enter__(2)

    pause(.5)
    enter__(2)




if __name__ == "__main__":
    iniciar()

