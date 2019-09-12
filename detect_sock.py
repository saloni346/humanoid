
import numpy as np
import io
import socket
import struct
import pickle
import cv2




server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server_socket.bind((socket.gethostname(),500))  # ADD IP HERE
server_socket.listen(0)

# Accept a single connection and make a file-like object out of it
conn,address = server_socket.accept()

face_cascade=cv2.CascadeClassifier(r"C:\Users\saloni garg\Documents\haarcascade_frontalface_default.xml")
eye_cascade=cv2.CascadeClassifier(r'C:\Users\saloni garg\Documents\haarcascade_eye.xml')

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
   
    faces=face_cascade.detectMultiScale(frame,1.3,5)
    for(x,y,w,h) in faces:
        cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
        #roi_gray=frame[y:y+h,x:x+w]
        roi_color=frame[y:y+h,x:x+w]
        eyes=eye_cascade.detectMultiScale(roi_color)
        for(ex,ey,ew,eh) in eyes:
            cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
            
    cv2.imshow('frame',frame)
    k=cv2.waitKey(30) & 0xff
    if k==27:
        break
        
cap.release()
cv2.destroyAllWindows()
server_socket.close()