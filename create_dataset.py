import cv2
import os

def generate_dataset(img,id,img_id):
    cv2.imwrite("C:/Users/saloni garg/Documents/dataset/user."+str(id)+"."+str(img_id)+".jpg",img)
def draw_boundary(img, classifier, scalefactor, minNeighbor, color,text):
    gray_img=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    features=classifier.detectMultiScale(gray_img,scalefactor,minNeighbor)
    coords = []

    for(x,y,w,h) in features:
        cv2.rectangle(img,(x,y),(x+w,y+h),color,2)
        cv2.putText(img,text,(x,y-4),cv2.FONT_HERSHEY_SIMPLEX,0.8,color,1,cv2.LINE_AA)
        coords = [x,y,w,h]
                    
    return coords,img
                                 
def detect(img,faceCascade,img_id):
    color={"blue":(255,0,0),"red":(0,0,255),"green":(0,255,0)}

    coords,img=draw_boundary(img,faceCascade,1.1,10,color['blue'],"face")
    if len(coords)==4:
        
        # Updating region of interest by cropping image
        roi_img = img[coords[1]:coords[1]+coords[3], coords[0]:coords[0]+coords[2]]
        
        generate_dataset(roi_img,i,img_id)
        # Passing roi, classifier, scaling factor, Minimum neighbours, color, label text
        #coords = draw_boundary(roi_img, eyeCascade, 1.1, 12, color['red'], "Eye")
    return img             
                    
faceCascade=cv2.CascadeClassifier(r'C:\Users\saloni garg\Documents\haarcascade_frontalface_default.xml') 
#eyeCascade = cv2.CascadeClassifier(r'C:\Users\saloni garg\Documents\haarcascade_eye.xml')
user_id={}
i=input("enter the id\n")
name=input("enter the name to the cooresponding id\n")
user_id[i]=name
video_capture=cv2.VideoCapture(0)

img_id=0
while True:
    _,img=video_capture.read()
    img=detect(img,faceCascade,img_id)
    cv2.imshow("face detection",img)
    img_id+=1
    if cv2.waitKey(1) & 0xFF==ord('q'):
        break
    
video_capture.release()
cv2.destroyAllWindows()