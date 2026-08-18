from time import sleep
from pyautogui import *
from pyperclip import copy
import mouse
from datetime import datetime, timedelta

def dia_hoje():
    return datetime.today().strftime("%d%m%Y")

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

def gerar_relatorio_faturamento_diario():
    """
    Executa a automação MTC255 para gerar o relatório de faturamento diário.
    """
    res = wait_enter()
    if not res:
        return False, "Processo cancelado pelo usuário."

    abrir_modulo("MTC255")
    pause(.5)

    tab()

    data = dia_hoje()
    write(data)
    write(data)

    tab(9)
    enter__(1)

    tab()
    enter__(1)

    return True, "Relatório de Faturamento Diário gerado com sucesso!"

if __name__ == "__main__":
    gerar_relatorio_faturamento_diario()
