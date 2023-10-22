import socket

BUFF = 65536
client_sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
client_sock.setsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF,BUFF)
host_name = socket.gethostname()
host_ip = socket.gethostbyname(host_name)
print('IP:',host_ip)
port = 9999

client_sock.sendto(b'oi',(host_ip,port))

while True:
    packet,_ = client_sock.recvfrom(BUFF)
    print('msg recebida:',packet.decode())
