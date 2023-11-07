from pynput import keyboard
from pynput.keyboard import Key, KeyCode
import sys
import socket
import time
import pickle

BUFF = 65536
CONNECTMSG = b'oi'
keys = []

def send(sock, clients, package):
    for addr in clients:
        try:
            sock.sendto(package,  addr)
        except Exception as e:
            #falhou em enviar msg
            pass

def check_new_clients(sock, clients):
    try: # Tenta receber mensagem
        client_msg,addr = sock.recvfrom(BUFF)
        if client_msg == CONNECTMSG:
            print('Novo cliente ouvindo: ',addr)
            clients.append(addr)
    except: # Caso falhe, não existem clientes novos
        return

def on_press(key):
    if keys.count(key) == 0:
        keys.append(key)
        # if key == keyboard.Key.esc:
        #     print('para de apertar esc')

def on_release(key):
    while keys.count(key) > 0:
        keys.remove(key)

def checkArguments():
    if (len(sys.argv) != 3):
        print("Quantidade incorreta de argumentos, forma de uso correta:")
        print(sys.argv[0] + " <porta> <delay entre mensagens (segundos)>")
        quit()
    try:
        port = int(sys.argv[1])
    except Exception as e:
        print("Porta deve ser um inteiro, forma de uso correta:")
        print(sys.argv[0] + " <porta> <delay entre mensagens (segundos)>")
        quit()
    try:
        delay = float(sys.argv[2])
    except:
        print("Delay entre mensagens deve ser um número real, forma de uso correta:")
        print(sys.argv[0] + " <porta> <delay entre mensagens (segundos)>")
        quit()
    return (port, delay)

def main(port, delay):
    print("Iniciando Servidor...")
    # Configura o socket
    sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF,BUFF)
    timeout = min(delay, 0.2)
    sock.settimeout(timeout)
    delay = delay - timeout
    print("Socket iniciado!")
    host_name = socket.gethostname()
    host_ip = socket.gethostbyname(host_name)
    sock_addr = (host_ip,port)
    sock.bind(sock_addr)

    print("IP: ", host_ip)
    print('Porta: ',port)

    # setup keyboard listener
    listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    listener.start()

    # main loop
    packCount = 1
    client_list = []
    while True:
        # envia proximo pacote
        package = (packCount, keys)
        print(f"Enviando pacote: {package}")
        package = pickle.dumps(package)
        send(sock, client_list, package)
        packCount += 1
        # Encerra envio caso tenha enviado ctrl+c
        if keys.count(Key.ctrl) > 0 and keys.count(KeyCode.from_char('c')) > 0:
            break
        # adiciona novos clientes
        check_new_clients(sock, client_list)
        time.sleep(delay)
    listener.stop()
    print("Encerrando servidor")
    print(f"{packCount} pacotes foram enviados")
    print(f"{len(client_list)} clientes foram adicionados a lista de envios")

if __name__ == '__main__':
    (port, delay) = checkArguments()
    main(port, delay)
