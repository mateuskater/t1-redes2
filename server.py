from pynput import keyboard
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

def receive(sock, clients):
    while True:
        try:
            client_msg,addr = sock.recvfrom(BUFF)
            if client_msg == CONNECTMSG:
                print('Novo cliente: ',addr)
                clients.append(addr)
            # if client_msg == b'cabou':
            # if client_msg == b'ack':
            # 	pacotes_recebidos+=1
        except:
            break

def on_press(key):
    if keys.count(key) == 0:
        keys.append(key)
    # if key == keyboard.Key.esc:
    #     return False

def on_release(key):
    while keys.count(key) > 0:
        keys.remove(key)

def main(port, delay):
    # Configures the socket
    sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF,BUFF)
    timeout = min(delay, 0.2)
    sock.settimeout(timeout)
    delay = delay - timeout
    host_name = socket.gethostname()
    host_ip = socket.gethostbyname(host_name)
    sock_addr = (host_ip,port)
    sock.bind(sock_addr)

    print("IP: ", host_ip)
    print('ouvindo ',sock_addr)

    # setup keyboard listener
    listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    listener.start()

    # main loop
    packCount = -1
    client_list = []
    while True:
        # makes the next package to be sent
        packCount += 1

        # sends next package in the sequence
        package = (packCount, keys)
        print("Package:")
        print(package)
        package = pickle.dumps(package)
        send(sock, client_list, package)

        # adds new clients
        receive(sock, client_list)
        time.sleep(delay)

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

if __name__ == '__main__':
    (port, delay) = checkArguments()
    main(port, delay)
