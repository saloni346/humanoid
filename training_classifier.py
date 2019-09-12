import numpy as np
from PIL import Image
import os
import cv2
data='C:/Users/saloni garg/Documents/dataset'
def train_Classifier(data):
    path=[os.path.join(data,f)for f in os.listdir(data)]
    faces=[]
    ids=[]
    
    for image in path:
        img=Image.open(image).convert('L')
        imageNp=np.array(img,'uint8')
        id=int(os.path.split(image)[1].split(".")[1])
        
        faces.append(imageNp)
        ids.append(id)
      
    ids=np.array(ids)
    
    #print(help(cv2.face))
    clf=cv2.face.LBPHFaceRecognizer_create()
    clf.train(faces,ids)
    clf.write("classifier.xml")
    
    
train_Classifier(data)