import face_recognition
import cv2
import os
import pickle
print(cv2.__version__)
flip=2

Encodings=[]
Names=[]
#Pre-trained model to recognize my face
with open('train.pkl','rb') as f:
    Names=pickle.load(f)
    Encodings=pickle.load(f)
font=cv2.FONT_HERSHEY_SIMPLEX
#camera params, create camera object
camSet='nvarguscamerasrc !  video/x-raw(memory:NVMM), width=3264, height=2464, format=NV12, framerate=21/1 ! nvvidconv flip-method='+str(flip)+' ! video/x-raw, width='+str(dispW)+', height='+str(dispH)+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink'
cam=cv2.VideoCapture(camSet)

while True:
    _,frame=cam.read()
    #converting colorspace from BGR (cv2 default) into RGB for face encodings
    frameRGB=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    facePositions=face_recognition.face_locations(frameRGB,model='cnn')
    allEncodings=face_recognition.face_encodings(frameRGB,facePositions)
    #checks all faces against pre-trained database, if no match returns 'unknown person'
    for (top,right,bottom,left),face_encodings in zip(facePositions,allEncodings):
        name='Unkown Person'
        matches=face_recognition.compare_faces(Encodings,face_encoding)
        if True in matches:
            first_match_index=matches.index(True)
            name=Names[first_match_index]
        cv2.rectangle(frame,(left,top),(bottom,right),(255,0,0),2)
        cv2.putText(frame,name,(left,top-6),font,.75,(0,0,255),2)
    cv2.imshow('Picture',frame)
    cv2.moveWindow('Picture',(0,0))
    if cv2.waitKey(1)==ord('q'):
        break
cv2.destroyAllWindows()
cam.release()
