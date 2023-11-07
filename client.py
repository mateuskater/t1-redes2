from pynput.keyboard import Controller, Key, KeyCode
import sys
import socket
import pickle

BUFF = 65536
CONNECTMSG = b'oi'
TIMEOUT = 1

def log(msg):
    print(msg)
    with open() as file:
        file.write(msg)
        
def checkArguments() -> tuple:
    '''Trata os argumentos passados na linha de comando'''
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

def main(server_ip, server_port):
    print('Iniciando cliente...')
    # Configura o socket
    sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF,BUFF)
    sock.settimeout(TIMEOUT)
    print("Socket iniciado!")
    print('IP: ',server_ip,server_port)

    print(f"Ouvindo {server_ip}, na porta {server_port}...")
    sock.sendto(CONNECTMSG ,(server_ip,server_port)) # envia msg de inicialização

    keyboard = Controller()
    oldKeys = []
    currPack = 0
    lostPacks = 0
    
    # recebe o primeiro pacote
    pack = sock.recv(BUFF)
    packNum, newKeys = pickle.loads(pack) # decodifica o pacote
    currPack = packNum
    firstPack = packNum
    print(f"Pacote {packNum} recebido.")
    while True:
        try:
            # Para programa se foi apertado ctrl+c no servidor
            if newKeys.count(Key.ctrl) > 0 and newKeys.count(KeyCode.from_char('c')) > 0:
                # Solta teclas que ainda estão pressionadas
                for key in newKeys:
                    keyboard.release(key)
                break

            for key in newKeys: # Pressiona as teclas que foram recebidas
                if oldKeys.count(key) == 0:
                    print(f"pressing {key}")
                    keyboard.press(key)
            for key in oldKeys: # Solta as teclas que foram recebidas
                if newKeys.count(key) == 0:
                    print(f"releasing {key}")
                    keyboard.release(key)
            oldKeys = newKeys
            if len(newKeys) > 0: # Imprime as teclas sendo pressionadas
                print(newKeys[0])

            pack = sock.recv(BUFF) # Recebe o pacote
            packNum, newKeys = pickle.loads(pack) # Decodifica o pacote
            lostPacks = lostPacks + (packNum - currPack - 1) # Contagem de pacotes perdidos, levando em conta o numero de sequência
            currPack = packNum # Atualiza o número de sequência do pacote
            print(f"Pacote {packNum} recebido.")
        except (socket.timeout, TimeoutError):
            print(f"A Conexão foi encerrada após atingir {str(TIMEOUT)} segundos de inatividade.")
    print()
    print('=================CLIENTE ENCERRADO=================')
    print(f"{currPack - firstPack - lostPacks} pacotes recebidos")
    print(f"{lostPacks} pacotes perdidos")
    print(f"Este cliente começou a receber a partir do pacote {firstPack}")
    print(f"Último pacote recebido por este cliente foi o de número {currPack}")

if __name__ == '__main__':
    (server_ip, server_port) = checkArguments()
    main(server_ip, server_port)
