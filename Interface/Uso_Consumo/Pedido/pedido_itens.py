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

def iniciar(itens, nf, data: str):
    print("Aguardando confirmação via mouse (x2 para continuar / x para cancelar)...")
    res = wait_enter()
    if not res:
        print("Automação de Pedidos cancelada pelo usuário.")
        return

    data_limpa = "".join(filter(str.isdigit, str(data)))

    click(x=103, y=74)  # BUSCA DE MODULOS
    modulo = "mtm138"
    for l in modulo:
        write(l)

    enter__()

    res = wait_enter()
    if not res:
        print("Automação de Pedidos cancelada pelo usuário.")
        return
    
    click(x=855, y=674)
    pause(2.5)
    enter__()

    for n in data_limpa:
        write(n)

    pause()


    res = wait_enter()
    if not res:
        print("Automação de Pedidos cancelada pelo usuário.")
        return

    enter__(1)
    write("225")
    enter__(1)
    write("3001")
    write("1")
    enter__(1)
    write("27")
    enter__(1)

    pause()
    click(x=320, y=92)
    pause()
    click(x=1037, y=583)

    for item in itens:
        hotkey("ctrl", "a", interval=0.2)
        descricao = item.get("descricao", "")
        print(f"Adicionando ao Pedido: {descricao}")

        write(descricao)
        enter__(1)

        click(x=535, y=146)

        res = wait_enter()
        if not res:
            print("Automação de Pedidos cancelada pelo usuário.")
            return

        enter__(1)
        pause(1)
        enter__(1)
        write("1")

        click(x=410, y=266)

        quantidade_fornecedor = str(item.get("quantidade", 0))
        write(quantidade_fornecedor)
        enter__()

        valor_unitario = str(item.get("valor_unitario", 0))
        write(valor_unitario)

        enter__(9)
        pause()
        press("down")
        press("down")

        moveTo(x=946, y=619)

        res = wait_enter()
        if not res:
            print("Automação de Pedidos cancelada pelo usuário.")
            return

        click(x=946, y=619)
        pause(0.5)

    press("esc")
    pause(0.5)
    press("esc")
    pause(1)

    click(x=403, y=92)
    obs = f"NF {nf}"
    write(obs)

    pause(0.5)
    click(x=485, y=96)

    for n in data_limpa:
        write(n)

    enter__()
    pause()

    moveTo(x=999, y=708)
    res = wait_enter()
    if not res:
        print("Automação de Pedidos cancelada pelo usuário.")
        return

    click(x=999, y=708)
    print("Pedido gerado com sucesso!")
