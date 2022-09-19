from tkinter import *
from tkinter import messagebox
import mysql.connector
import threading
import trace
import threading
import numpy as np
import cv2 
import sys
import tkinter
from PIL import Image,ImageTk
import time

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="root",
  database = "attendance"
)
sql = mydb.cursor()

classidE =''
passwordE = ''
teacher = ''
temail = ''
Class = ''


def inputcheck():

    global loginbutton
    global root2
    global classidE
    global passwordE
    while True:
        lock.acquire()

            
        classidd = classidE.get()

        passwordd = passwordE.get()
    

        if classidd == "" or passwordd == "":
            loginbutton.config(state="disabled")
            loginbutton.place(relx=0.5, rely=0.6, anchor=CENTER)
        if classidd !="" and passwordd !="":
            loginbutton.config(state="normal")
            loginbutton.place(relx=0.5, rely=0.6, anchor=CENTER)
        lock.release()

        




#taking data from database
def login():
    global Class
    global teacher
    global temail

    alert = False
    exit1 = False
    classid2 =''
    password2 =''

    classid = classidE.get()
    password = passwordE.get()

    sql.execute(f"SELECT loginid FROM login WHERE loginid ='{classid}'")
    
    result = sql.fetchall()
    for x in result:
        classid2 = x[0]

    sql.execute(f"SELECT passwordd FROM login WHERE loginid = '{classid}'")
    result = sql.fetchall()
    for x in result:
        password2 = x[0]

    sql.execute(f"SELECT teacher FROM login WHERE loginid = '{classid}'")
    result = sql.fetchall()
    for x in result:
        teacher = x[0]

    sql.execute(f"SELECT class FROM login WHERE loginid = '{classid}'")
    result = sql.fetchall()
    for x in result:
        Class = x[0]

    sql.execute(f"SELECT teacheremail FROM login WHERE loginid = '{classid}'")
    result = sql.fetchall()
    for x in result:
        temail = x[0]


    if len(classid) ==0:
        alert = True
    if len(password) == 0:
        alert = True
    if classid != classid2:
        alert = True
    if password != password2:
        alert = True

    if alert == True:
        messagebox.showerror("Error", "Incorrect login id or password!")

    if alert == False:
        root2.destroy()
        t2.kill()
        main()

    
def killthread():
    t1.kill()
    sys.exit()

def loginpage():
    lock.acquire()
    global root2
    global classidE
    global passwordE
    global loginbutton
#----------LOG IN PAGE-------

#canvas and page setting
    root2 = Tk()
    canvas2 = Canvas(root2, height=700, width=800)
    canvas2.pack()
#classidE input widget
    classid = Label(root2, text="login ID:")
    classid.place(relx=0.2, rely=0.38)
    classidE = Entry(root2, width=50)
    classidE.pack()
    classidE.place(relx=0.5, rely=0.38, anchor=CENTER)

    #password input widget
    password = Label(root2, text="Password:")
    password.place(relx=0.2, rely=0.48)
    passwordE = Entry(root2, width=50)
    passwordE.config(show="*")
    passwordE.pack()
    passwordE.place(relx=0.5, rely=0.5, anchor=CENTER)



    #continue button 
    loginbutton = Button(root2, text="Log in", width= 20, pady=25, command = login)
    loginbutton.place(relx=0.5, rely=0.6, anchor=CENTER)

    lock.release()
    root2.mainloop()

def main():
    global root
    
#----------MAIN PAGE---------------------
    #Canvas and page settings
    root = Tk()
    root.protocol("WM_DELETE_WINDOW", killthread)
    canvas = Canvas(root, height=700, width=800)
    canvas.pack()
    #

    classlabel = Label(root, text = f"Hello {Class}", font=('arial', 20), fg='red')
    classlabel.place(relx=0.5, rely=0.2, anchor= CENTER)

    instructlabel = Label(root, text="Please select method of attendance.", font=("arial", 15))
    instructlabel.place(relx=0.5, rely=0.3, anchor= CENTER)

    fingerprint = Button(root, text="Fingerprint", padx=30, pady=30)
    fingerprint.place(relx=0.1, rely=0.5)

    face_id = Button(root, text="Face Recognition and OTP", padx=20, pady=20, command=face)
    face_id.place(relx=0.4, rely=0.5)

    qr_code = Button(root, text="QR Code", padx=30, pady=30)
    qr_code.place(relx=0.8, rely=0.5)

    root.mainloop()


def facecam():
    root3.destroy()
    root.destroy()

#this is a face detection pg, it will detect ur face and capture a pic of ur face 

    cap = cv2.VideoCapture(0)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
    root4 = Tk()
    camera1 = Label(root4)
    camera1.pack()

    countdown = time.time() +5

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
            #cv2.imwrite("image2.png", roi_grey) #string variable inside is the file classide of ur capture face

            #cv2.imshow('frame', frame)
            img = ImageTk.PhotoImage(Image.fromarray(frame))
            camera1.configure(image = img)
            camera1.update()

        if time.time() >= countdown:
            print("here")
            cv2.imwrite("image2.png", roi_grey) #string variable inside is the file classide of ur capture face
            root4.destroy()
            break
        root4.update()


    root4.mainloop()

    cap.release()
    cv2.destroyAllWindows()  


def face():
    global root3
    #canvas and page setting
    root3 = Tk()
    canvas3 = Canvas(root3, height=700, width=800)
    canvas3.pack()

#----------FACE RECOGNITION PAGE----------

#face cam activation screen
    button = Button(root3, text="Click to activate camera", padx=50, pady=50, command=facecam)
    button.place(relx=0.5, rely=0.5, anchor=CENTER)

    root3.mainloop()


#threading
lock = threading.Lock()


class thread_with_trace(threading.Thread):
  def __init__(self, *args, **keywords):
    threading.Thread.__init__(self, *args, **keywords)
    self.killed = False
 
  def start(self):
    self.__run_backup = self.run
    self.run = self.__run     
    threading.Thread.start(self)
 
  def __run(self):
    sys.settrace(self.globaltrace)
    self.__run_backup()
    self.run = self.__run_backup
 
  def globaltrace(self, frame, event, arg):
    if event == 'call':
      return self.localtrace
    else:
      return None
 
  def localtrace(self, frame, event, arg):
    if self.killed:
      if event == 'line':
        raise SystemExit()
    return self.localtrace
 
  def kill(self):
    self.killed = True
 
t1 = thread_with_trace(target = loginpage)
t2 = thread_with_trace(target = inputcheck)

t1.start()
t2.start()
t1.join()
t2.join()


#loginpage()

#main()
#face()
