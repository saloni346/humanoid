import io
import socket
import struct
import pickle
import cv2
import numpy as np

server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
#server_socket.bind((socket.gethostname(),500))  # ADD IP HERE
server_socket.bind(('192.168.43.95',500))
server_socket.listen(0)

# Accept a single connection and make a file-like object out of it
conn,address = server_socket.accept()


def draw_boundary(img, classifier, scaleFactor, minNeighbors, color, text, clf):
    #gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    features = classifier.detectMultiScale(img, scaleFactor, minNeighbors)
    coords = []

   
    for (x, y, w, h) in features:
        cv2.rectangle(img, (x,y), (x+w, y+h), color, 2)
        id, _ = clf.predict(img[y:y+h, x:x+w])
        if id == 1:
            cv2.putText(img, "saloni", (x, y-4), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 1, cv2.LINE_AA)
            #conn.send(str(id).encode("utf-8"))
        if id == 2:
            cv2.putText(img, "faraz", (x, y-4), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 1, cv2.LINE_AA)
            #conn.send(str(id).encode("utf-8"))
        if id == 3:
            cv2.putText(img, "saad", (x, y-4), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 1, cv2.LINE_AA)
            #conn.send(str(id).encode("utf-8"))
        if id == 4:
            cv2.putText(img, "himanshi", (x, y-4), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 1, cv2.LINE_AA)
        conn.send(str(id).encode("utf-8"))
        coords = [x, y, w, h]
    return coords



def recognize(img, clf, faceCascade):
    color = {"black":(0,0,0),"blue": (255, 0, 0), "red": (0, 0, 255), "green": (0, 255, 0), "white": (255, 255, 255)}
    coords = draw_boundary(img, faceCascade, 1.1, 10, color["green"], "Face", clf)
    return img



faceCascade = cv2.CascadeClassifier(r'C:\Users\saloni garg\Documents\haarcascade_frontalface_default.xml')


clf = cv2.face.LBPHFaceRecognizer_create()
clf.read('classifier.xml')


data = b''
payload_size = struct.calcsize("L")

while True:
    while len(data) < payload_size:
        data += conn.recv(8000)
    packed_msg_size = data[:payload_size]

    data = data[payload_size:]
    msg_size = struct.unpack("L", packed_msg_size)[0]

    while len(data) < msg_size:
        data += conn.recv(8000)
    frame_data = data[:msg_size]
    data = data[msg_size:]

    frame=pickle.loads(frame_data)
       
    img = recognize(frame, clf, faceCascade)
    
    cv2.imshow("face detection", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
    #if not frame:
        break

server_socket.close()