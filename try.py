from tkinter import *
from tkinter import messagebox
import mysql.connector
import threading
import trace
import threading
import numpy as np
import cv2 
import sys
from PIL import Image,ImageTk


cap = cv2.VideoCapture(0)
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
root4 = Tk()
camera = Label(root4)
teee = Label(root4, text="hello world")
camera.pack()
teee.pack()

while True:
    ret, frame = cap.read() ##
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) ##
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    for (x, y, w, h) in faces:
        
        cv2.rectangle(frame, (x, y), (x + w, y + h), (500, 0, 0), 5)
        roi_grey = gray[y: y+w, x:x+w] 
        roi_color = frame[y:y+h, x:x+h]
        eyes = eye_cascade.detectMultiScale(roi_grey, 1.3, 5)
        for (ex, ey, ew, eh) in eyes:
            cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey +eh), (0, 300, 0), 5)
        cv2.imwrite("image2.png", roi_grey) #string variable inside is the file classide of ur capture face

        #cv2.imshow('frame', frame)

        img = ImageTk.PhotoImage(Image.fromarray(frame))
        camera.configure(image = img)
        camera.update()

    if cv2.waitKey(1) == ord('q'):
        break
    root4.update()

cap.release()
cv2.destroyAllWindows()  
