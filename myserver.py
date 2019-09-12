import io
import socket
import struct
import pickle
import cv2

server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
#server_socket.bind((socket.gethostname(),500))  # ADD IP HERE
server_socket.bind(('192.168.100.25',500))
server_socket.listen(0)

# Accept a single connection and make a file-like object out of it
conn,address = server_socket.accept()
data = b''
payload_size = struct.calcsize("L")

while True:
    while len(data) < payload_size:
        data += conn.recv(4096)
    packed_msg_size = data[:payload_size]

    data = data[payload_size:]
    msg_size = struct.unpack("L", packed_msg_size)[0]

    while len(data) < msg_size:
        data += conn.recv(4096)
    frame_data = data[:msg_size]
    data = data[msg_size:]

    frame=pickle.loads(frame_data)
    print(frame.size)
    cv2.imshow('frame', frame)
    k=cv2.waitKey(30) & 0xff
    if k==27:
        break

server_socket.close()