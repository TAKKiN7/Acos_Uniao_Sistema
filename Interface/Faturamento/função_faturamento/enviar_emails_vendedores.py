from time import sleep
from pyautogui import *
from pyperclip import copy
import mouse
from datetime import datetime, timedelta

def dia_anterior():
    dias = 3 if datetime.today().weekday() == 0 else 1
    return (datetime.today() - timedelta(days=dias)).strftime("%d%m%Y")

def pause(time=0.3):
    sleep(time)

def tab(times : int = 1):
    for c in range(times):
        press("tab")

def enter__(times=2, time=0):
    for c in range(times):
        press("enter")
        sleep(time)

def wait_enter():
    while True:
        if mouse.is_pressed("x2"):
            return True
        elif mouse.is_pressed("x"):
            return False
        sleep(0.1)  # Pequena pausa para não sobrecarregar o CPU

def abrir_modulo(modulo : str):
    press("F5")
    write(modulo)
    enter__()

def enviar_emails_vendedores():
    """
    Executa a automação MTR312 para gerar e enviar e-mails aos vendedores.
    """
    res = wait_enter()
    if not res:
        return False, "Processo cancelado pelo usuário."

    abrir_modulo("MTR312")
    pause(.5)

    data = dia_anterior()
    write(data)
    pause()
    write(data)

    tab(8)
    pause()
    enter__(1)
    pause(1)

    tab(7)
    press("space")
    tab()
    enter__(1)

    res = wait_enter()
    if not res:
        return False, "Processo cancelado pelo usuário."

    tab(2)
    pause()
    enter__(1)

    return True, "Envio de e-mails para vendedores concluído com sucesso!"

if __name__ == "__main__":
    enviar_emails_vendedores()
