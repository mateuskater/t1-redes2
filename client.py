from pynput.keyboard import Controller
import sys
import socket
import pickle

BUFF = 65536
CONNECTMSG = b'oi'

def connect(sock, server):
    sock.sendto(CONNECTMSG ,server)

def receive(sock):
    pack,_ = sock.recvfrom(BUFF)
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

def main(server_ip, server_port):
    # Configures socket
    sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF,BUFF)
    # host_name = socket.gethostname()
    # host_ip = socket.gethostbyname(host_name)
    print('IP:',(server_ip,server_port))

    # Connects to server
    connect(sock, (server_ip, server_port))

    # Listens to server
    keyboard = Controller()
    oldKeys = []
    while True:
        pack = receive(sock)
        packNum, newKeys = pickle.loads(pack)
        for key in newKeys:
            print("pressing")
            if oldKeys.count(key) == 0:
                print(key)
                keyboard.press(key)
        for key in oldKeys:
            print("releasing")
            if newKeys.count(key) == 0:
                print(key)
                keyboard.release(key)
        oldKeys = newKeys


if __name__ == '__main__':
    (server_ip, server_port) = checkArguments()
    main(server_ip, server_port)
