import io
import socket
import struct
import cv2
import pickle

client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

client_socket.connect((socket.gethostname(),500))  # ADD IP HERE

# Make a file-like object out of the connection
    # Start a preview and let the camera warm up for 2 seconds
cap=cv2.VideoCapture(0)
    # Note the start time and construct a stream to hold image data
    # temporarily (we could write it directly to connection but in this
    # case we want to find out the size of each capture first to keep
    # our protocol simple)
while True:
    ret,img=cap.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    data = pickle.dumps(gray)
    client_socket.sendall(struct.pack("L", len(data)) + data)
    

    cv2.imshow('img',img)
    k=cv2.waitKey(30) & 0xff
    if k==27:
        break

client_socket.close()
cap.release()
cv2.destroyAllWindows()
