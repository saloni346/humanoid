import socket

s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
#host=socket.gethostname()
s.connect((socket.gethostname(),500))
message=input("->")
s.send(message.encode("utf-8"))
msg=s.recv(1024)
print(msg.decode("utf-8"))
s.close()