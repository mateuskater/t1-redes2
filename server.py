import sys
import socket
import time

BUFF = 65536
def send(clients, pacote):
    for addr in clients:
        try:
            sock.sendto(str(pacote).encode(), addr)
        except Exception as e:
            #falhou em enviar msg
            pass



def recieve(clients):
    while True:
        try:
            client_msg,addr = sock.recvfrom(BUFF)
            if client_msg == b'oi':
                print('Novo cliente: ',addr)
                clients.append(addr)
            # if client_msg == b'cabou':
            # if client_msg == b'ack':
            # 	pacotes_recebidos+=1
        except:
            break

def main():
    pacotes_enviados = 0
    client_list = []
    while True:
        send(client_list, pacotes_enviados)
        pacotes_enviados += 1
        recieve(client_list)

    time.sleep(delay)

if __name__ == '__main__':
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

    sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF,BUFF)
    sock.settimeout(0.2)
    host_name = socket.gethostname()
    host_ip = socket.gethostbyname(host_name)
    print("IP: ", host_ip)
    sock_addr = (host_ip,port)
    sock.bind(sock_addr)
    print('ouvindo ',sock_addr)
    main()
