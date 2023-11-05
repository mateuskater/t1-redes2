from pynput.keyboard import Controller
import sys
import socket
import pickle

BUFF = 65536
CONNECTMSG = b'oi'

def connect(sock, server):
    sock.sendto(CONNECTMSG ,server)

def receive(sock: socket.socket):
    pack = sock.recv(BUFF)
    return pack

def checkArguments():
    if (len(sys.argv) != 3):
        print("Quantidade incorreta de argumentos, forma de uso correta:")
        print(sys.argv[0] + " <ip server> <porta server>")
        quit()
    try:
        server_port = int(sys.argv[2])
    except Exception as e:
        print("Porta deve ser um inteiro, forma de uso correta:")
        print(sys.argv[0] + " <ip server> <porta server>")
        quit()
    server_ip = sys.argv[1]

    return (server_ip, server_port)

def log(msg):
    print(msg)
    with open('log.txt', 'w') as file:
        file.write(msg)

def main(server_ip, server_port):
    print('Iniciando cliente...')
    # Configures socket
    sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF,BUFF)
    print("Socket iniciado!")
    # host_name = socket.gethostname()
    # host_ip = socket.gethostbyname(host_name)
    print('IP: ',server_ip,server_port)

    # Connects to server
    print(f"Conectando a {server_ip}, porta {server_port}...")
    try:
        connect(sock, (server_ip, server_port))
    except Exception as e:
        print(e)
        input()
        exit()

    print("Conectado!")

    # Listens to server
    keyboard = Controller()
    oldKeys = []
    currPack = 0
    lostPacks = 0
    try:
        while True:
            pack = receive(sock)
            packNum, newKeys = pickle.loads(pack)
            lostPacks = lostPacks + (packNum - currPack + 1)
            currPack = packNum
            print(f"Pacote {packNum} recebido.")
            for key in newKeys:
                if oldKeys.count(key) == 0:
                    print(f"pressing {key}")
                    keyboard.press(key)
            for key in oldKeys:
                if newKeys.count(key) == 0:
                    print(f"releasing {key}")
                    keyboard.release(key)
            oldKeys = newKeys
        print(f"Pacotes perdidos: {lostPacks}")
    except ConnectionResetError:
        print("cabou")

if __name__ == '__main__':
    (server_ip, server_port) = checkArguments()
    main(server_ip, server_port)
