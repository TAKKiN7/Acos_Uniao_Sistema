from time import sleep
from pyautogui import press, write, click, hotkey, moveTo
from pyperclip import copy
import mouse

def pause(time=0.3):
    sleep(time)

def enter__(times=2, time=0):
    for _ in range(times):
        press("enter")
        sleep(time)

def wait_enter():
    while True:
        if mouse.is_pressed("x2"):
            return True
        if mouse.is_pressed("x"):
            return False
        sleep(0.1)

def iniciar(itens):
    print("Aguardando confirmação via mouse (x2 para continuar / x para cancelar)...")
    res = wait_enter()
    if not res:
        print("Automação cancelada pelo usuário.")
        return

    click(x=103, y=74)  # BUSCA DE MODULOS
    modulo = "mtm171"
    for l in modulo:
        write(l)

    enter__()

    res = wait_enter()
    if not res:
        print("Automação cancelada pelo usuário.")
        return
    
    click(x=27, y=152)
    pause()
    click(x=27, y=152)
    pause(3)
    click(x=794, y=465)

    res = wait_enter()
    if not res:
        print("Automação cancelada pelo usuário.")
        return

    for item in itens:
        enter__(1)
        descricao = item.get("descricao", "")
        print(f"Cadastrando: {descricao}")

        copy(descricao)
        hotkey("ctrl", "v", interval=0.2)
        enter__()
        write("6")
        enter__(1)
        write("9")
        enter__(3)
        unidade: str = str(item.get("unidade", ""))
        write(unidade.lower())
        enter__(1)
        write('1')
        enter__(1)
        write('1')
        enter__(4)

        write(item.get("ncm_sh", ""))

        click(x=797, y=304)
        pause()
        click(x=752, y=343)

        moveTo(x=927, y=660)

        res = wait_enter()
        if not res:
            print("Automação cancelada pelo usuário.")
            return

    print("Cadastro concluído com sucesso!")
