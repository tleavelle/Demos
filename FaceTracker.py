import cv2
print(cv2.__version__)
dispW=640
dispH=480
flip=2
from adafruit_servokit import ServoKit
kit=ServoKit(channels=16)
pan=90
tilt=90
kit.servo[0].angle=pan
kit.servo[1].angle=tilt
#setting camera params and creating camera object
camSet='nvarguscamerasrc !  video/x-raw(memory:NVMM), width=3264, height=2464, format=NV12, framerate=21/1 ! nvvidconv flip-method='+str(flip)+' ! video/x-raw, width='+str(dispW)+', height='+str(dispH)+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink'
cam= cv2.VideoCapture(camSet)
#Pre-trained haarcascades to detect eyes and faces
face_cascade=cv2.CascadeClassifier('/home/tleavelle97/Desktop/pyPro/cascade/face.xml')
eye_cascade=cv2.CascadeClassifier('/home/tleavelle97/Desktop/pyPro/cascade/eye.xml')
#whle loop continually reads camera into frame, and determines servo position
#Based on a error offset from centerpoint of region of interest (the face)
while True:
    ret, frame = cam.read()
    gray=cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces=face_cascade.detectMultiScale(gray,1.3,5)
    for (x,y,w,h) in faces:
        Xcent=x+w/2
        Ycent=y+h/2
        errorPan=Xcent-dispW/2
        errorTilt=Ycent-dispH/2
        if abs(errorPan)>15:
            pan=pan-errorPan/50
        if abs(errorTilt)>15:
            tilt=tilt-errorTilt/50
        if pan>180:
            pan=180
            print("Servo has reached its limit")
        if pan<0:
            pan=0
            print("Servo has reached its limit")
        if tilt>180:
            tilt=180
            print("Servo has reached its limit)
        if tilt<0:
            tilt=0
            print("Servo has reached its limit")
        kit.servo[0].angle=pan
        kit.servo[1].angle=tilt

        roi_gray=gray[y:y+h,x:x+w]
        roi_color=frame[y:y+h,x:x+w]
        eyes=eye_cascade.detectMultiScale(roi_gray)
        for (ex,ey,ew,eh) in eyes:
            cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(255,0,0),2)
        break
    frame=cv2.resize(frame,(640,480))
    cv2.imshow('nanoCam',frame)
    cv2.moveWindow('nanoCam',0,0)
    #end program by pressing 'q', clean up scripts
    if cv2.waitKey(1)==ord('q'):
        break
cam.release()
cv2.destroyAllWindows()