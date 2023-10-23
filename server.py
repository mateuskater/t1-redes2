import sys
import socket
import time

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

BUFF = 65536
sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF,BUFF)
sock.settimeout(0.2)
host_name = socket.gethostname()
host_ip = socket.gethostbyname(host_name)
print("IP: ", host_ip)
sock_addr = (host_ip,port)
sock.bind(sock_addr)
print('ouvindo ',sock_addr)

pacotes_enviados = 0
client_list = []

while True:
    for addr in client_list:
        try:
            sock.sendto(str(pacotes_enviados).encode(), addr)
        except Exception as e:
            #falhou em enviar msg
            pass
    pacotes_enviados += 1

    while True:
        try:
            client_msg,addr = sock.recvfrom(BUFF)
            if client_msg == b'oi':
                print('Novo cliente: ',addr)
                client_list.append(addr)
            # if client_msg == b'cabou':
            # if client_msg == b'ack':
            # 	pacotes_recebidos+=1
        except:
            break
    time.sleep(delay)
