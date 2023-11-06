from pynput.keyboard import Controller, Key, KeyCode
import sys
import socket
import pickle

BUFF = 65536
CONNECTMSG = b'oi'

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
    # Configura o socket
    sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF,BUFF)
    sock.settimeout(20)
    print("Socket iniciado!")
    print('IP: ',server_ip,server_port)

    print(f"Ouvindo {server_ip}, na porta {server_port}...")
    sock.sendto(CONNECTMSG ,(server_ip,server_port)) # envia msg de inicialização

    keyboard = Controller()
    oldKeys = []
    currPack = 0
    lostPacks = 0
    
    # recebe o primeiro pacote
    pack = receive(sock)
    packNum, newKeys = pickle.loads(pack)
    currPack = packNum
    firstPack = packNum
    print(f"Pacote {packNum} recebido.")
    try:
        while True:
            # Para programa se foi apertado ctrl+c no servidor
            if newKeys.count(Key.ctrl) > 0 and newKeys.count(KeyCode.from_char('c')) > 0:
                # Solta teclas que ainda estão pressionadas
                for key in newKeys:
                    keyboard.release(key)
                break

            for key in newKeys:
                if oldKeys.count(key) == 0:
                    print(f"pressing {key}")
                    keyboard.press(key)
            for key in oldKeys:
                if newKeys.count(key) == 0:
                    print(f"releasing {key}")
                    keyboard.release(key)
            oldKeys = newKeys
            if len(newKeys) > 0:
                print(newKeys[0])

            pack = receive(sock)
            packNum, newKeys = pickle.loads(pack)
            lostPacks = lostPacks + (packNum - currPack - 1)
            currPack = packNum
            print(f"Pacote {packNum} recebido.")
    except TimeoutError:
        print("A Conexão foi encerrada após atingir 20 segundos de inatividade.")
        # print('Total de pacotes recebidos: ')
        print(f"Pacotes perdidos: {lostPacks}")
    except ConnectionResetError: 
        print('faiou')
    
    print("Servidor encerrou a transmissão")
    print(f"{currPack - firstPack - lostPacks} pacotes recebidos")
    print(f"{lostPacks} pacotes perdidos")
    print(f"Este cliente começou a receber a partir do pacote {firstPack}")
    print(f"Último pacote recebido por este cliente foi o de número {currPack}")

if __name__ == '__main__':
    (server_ip, server_port) = checkArguments()
    main(server_ip, server_port)
