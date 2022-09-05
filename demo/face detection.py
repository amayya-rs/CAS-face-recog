import numpy as np
import cv2 
import sys

#this is a face detection pg, it will detect ur face and capture a pic of ur face 

cap = cv2.VideoCapture(0)
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

while True:
    ret, frame = cap.read()
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    for (x, y, w, h) in faces:
        
        cv2.rectangle(frame, (x, y), (x + w, y + h), (500, 0, 0), 5)
        roi_grey = gray[y: y+w, x:x+w] 
        roi_color = frame[y:y+h, x:x+h]
        eyes = eye_cascade.detectMultiScale(roi_grey, 1.3, 5)
        for (ex, ey, ew, eh) in eyes:
            cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey +eh), (0, 300, 0), 5)
        cv2.imwrite("image2.png", roi_grey) #string variable inside is the file name of ur capture face

        cv2.imshow('frame', frame)

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()