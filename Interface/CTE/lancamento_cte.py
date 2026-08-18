from time import sleep
from pyautogui import press, click, write, hotkey
import mouse
from tkinter import messagebox as msg

def pause(time=0.5):
    sleep(time)

def enter__(times=2, time=0):
    for _ in range(times):
        press("enter")
        sleep(time)

def wait_enter():
    while True:
        if mouse.is_pressed("x2"):
            return True  # Continua quando o botão X2 do mouse for pressionado
        if mouse.is_pressed("x"):
            return False # Cancela se o botão X do mouse for pressionado
        sleep(0.1)

def executar_lancamento_cte(data: str, user: str = "tk", parent=None):
    """
    Executa a automação de lançamento de Notas CTE.
    Aguardará os botões do mouse (X2 para prosseguir / X para cancelar).
    """
    # Remove barras e caracteres não numéricos para a digitação da data
    data_limpa = "".join(filter(str.isdigit, data)) if data else data

    msg.showwarning("Atenção", f"Data de vencimento configurada: {data}", parent=parent)

    res = wait_enter()
    if not res:
        print("Lançamento CTE cancelado pelo usuário.")
        return

    press("F5")
    write("MTP451")
    enter__()
    pause(.4)

    enter__(2, 0.2)

    while True:
        res = wait_enter()
        if not res:
            print("Loop de itens CTE encerrado pelo usuário.")
            break

        enter__(1)
        pause(0.5)
        click(x=324, y=391)
        pause()
        click(x=300, y=487)
        pause()
        click(x=301, y=416)
        pause()
        click(x=308, y=447)
        pause()
        click(x=1018, y=611)
        pause(1)

        hotkey("ctrl", "t", interval=0.2)
        pause()
        write("1")
        enter__(time=0.5)
        pause(1)

        for n in data_limpa:
            write(n)

        pause()
        enter__(3)

        pause()

        for c in range(3):
            press("tab")

        pause()
        enter__(1)

        press("down")

    msg.showinfo("FINALIZAÇÃO", "Aguardando finalização", parent=parent)
    res = wait_enter()
    if not res:
        print("Finalização CTE cancelada pelo usuário.")
        return

    click(x=843, y=621)
    pause()
    click(x=1169, y=678)
    print("Lançamento CTE concluído!")
