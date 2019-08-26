import socket

s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
#host=socket.gethostname()
s.bind((socket.gethostname(),500))
s.listen(5)

clientsocket,address=s.accept()
print(f"connection from{address}has been established!")
msg=clientsocket.recv(1024)
msg1=msg.decode("utf-8")
d={'1':'saloni', '2':'abc', '3':'cde'}
clientsocket.send(d[msg1].encode("utf-8"))
clientsocket.close()
s.close()