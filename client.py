import sys
import socket

if (len(sys.argv) != 3):
    print("Quantidade incorreta de argumentos, forma de uso correta:")
    print(sys.argv[0] + " <ip server> <porta server>")
    quit()

server_ip = sys.argv[1]

try:
    server_port = int(sys.argv[2])
except Exception as e:
    print("Porta deve ser um inteiro, forma de uso correta:")
    print(sys.argv[0] + " <ip server> <porta server>")
    quit()

BUFF = 65536
client_sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
client_sock.setsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF,BUFF)
host_name = socket.gethostname()
host_ip = socket.gethostbyname(host_name)
print('IP:',(server_ip,server_port))
port = 9999

client_sock.sendto(b'oi',(server_ip,server_port))

while True:
    packet,_ = client_sock.recvfrom(BUFF)
    print('msg recebida:',packet.decode())
