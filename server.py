import socket
import time

BUFF = 65536
sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF,BUFF)
sock.settimeout(0.2)
host_name = socket.gethostname()
host_ip = socket.gethostbyname(host_name)
print("IP: ", host_ip)
port = 9999
sock_addr = (host_ip,port)
sock.bind(sock_addr)
print('ouvindo ',sock_addr)

pacotes_recebidos = 0
client_list = []

while True:
	msg = input()
	for addr in client_list:
		try:
			sock.sendto(msg.encode(), addr)
		except Exception as e:
			#falhou em enviar msg
			pass

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
	time.sleep(0.1)
