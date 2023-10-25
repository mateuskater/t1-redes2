import sys
import socket
import time

BUFF = 65536
CONNECTMSG = b'oi'
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

def main(port, delay):
    # Configures the socket
    sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF,BUFF)
    sock.settimeout(0.2)
    host_name = socket.gethostname()
    host_ip = socket.gethostbyname(host_name)
    sock_addr = (host_ip,port)
    sock.bind(sock_addr)

    print("IP: ", host_ip)
    print('ouvindo ',sock_addr)
    # main loop
    packCount = -1
    client_list = []
    while True:
        # makes the next package to be sent
        packCount += 1

        # sends next package in the sequence
        send(sock, client_list, str(packCount).encode())

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
