import io
import socket
import struct
import cv2
import pickle

client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

client_socket.connect((socket.gethostname(),500))  # ADD IP HERE


face_cascade=cv2.CascadeClassifier(r"C:\Users\saloni garg\Documents\haarcascade_frontalface_default.xml")
#eye_cascade=cv2.CascadeClassifier(r'C:\Users\saloni garg\Documents\haarcascade_eye.xml')

# Make a file-like object out of the connection
    # Start a preview and let the camera warm up for 2 seconds
cap=cv2.VideoCapture(0 + cv2.CAP_DSHOW)
    # Note the start time and construct a stream to hold image data
    # temporarily (we could write it directly to connection but in this
    # case we want to find out the size of each capture first to keep
    # our protocol simple)
while True:
    ret,img=cap.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    data = pickle.dumps(gray)
    client_socket.sendall(struct.pack("L", len(data)) + data)
    data= client_socket.recv(1024)
    id=data.decode("utf-8")

    faces=face_cascade.detectMultiScale(gray,1.3,5)
    for(x,y,w,h) in faces:
        cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
        cv2.putText(img, id, (x, y-4), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 1, cv2.LINE_AA)
        #roi_gray=frame[y:y+h,x:x+w]
        #roi_color=img[y:y+h,x:x+w]
        #eyes=eye_cascade.detectMultiScale(roi_color)
        #for(ex,ey,ew,eh) in eyes:
            #cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)

    cv2.imshow('img',img)
    k=cv2.waitKey(30) & 0xff
    if k==27:
        break

client_socket.close()
cap.release()
cv2.destroyAllWindows()
