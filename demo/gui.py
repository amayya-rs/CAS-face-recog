from datetime import datetime
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
import time
import os
import face_recognition
import random
import string
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


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
todaydate = datetime.now().strftime('%d_%B_%Y') 
 

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

        
def createdatabaseattendance():
    try:
        sql.execute(f"create table {todaydate}_{Class} (name varchar(30), time varchar(30), late boolean);")
    except:
        pass


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
        createdatabaseattendance()
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



def infoo():
    messagebox.showinfo("Information", "Camera will close 5 seconds after it opens! Look onto the camera once its opened!")

def resetvalue():
    global name
    messagebox.showinfo("Attendance Updated", "your attendance has been updated! Thank you for your attendance")
    name = ''
    main()

def updatedatabase():
    currtime = datetime.now().strftime("%H:%M:%S")
    currtime2 = datetime.now()
    latetime = currtime2.replace(hour = 7, minute = 30, second = 0)
    late = False
    if currtime2 > latetime:
        late = True
    sql.execute(f"insert into {todaydate}_{Class} Values ('{name}', '{currtime}', {late});")
    late = False
    sendconfimation()
    
def sendconfimation():
    sql.execute(f"select email from {Class} where fullname = '{name}';")
    result = sql.fetchall()
    revemail = ''
    for i in result:
        revemail = i[0]

    email = "pythonbot123@outlook.com" #sender email
    password = "TanMichaelOlsen2006" #sender email password
    receiver = revemail #receiver email 
    server = smtplib.SMTP('smtp.office365.com', 587)
    server.ehlo()
    server.starttls()
    server.login(email, password)

    

    msg = MIMEMultipart()
    msg['Subject'] = "Attendance Confimation"
    msg['To'] = receiver
    msg['From'] = email
    body = f"Hello {name}! Your attendance has been succesfully taken! if your teacher marks you absent, you can show this email as a prove that you are present. \n Attendance Date {datetime.now().strftime('%d %B %Y %H:%M:%S')} \n please contact the developers if there are errors on the program."
    msg.attach(MIMEText(body))

    tobesend = msg.as_string()
    server.sendmail(email, receiver, tobesend)
    server.quit()
    resetvalue()


def authentication():
    global root5
    global message2
    code2 = ''
    global count
    count = 5

    def sendcode(text):
        print(Class)
        sql.execute(f"select email from {Class} where fullname = '{name}';")
        result = sql.fetchall()
        revemail = ''
        for i in result:
            revemail = i[0]

        email = "pythonbot123@outlook.com" #sender email
        password = "TanMichaelOlsen2006" #sender email password
        receiver = revemail #receiver email 
        server = smtplib.SMTP('smtp.office365.com', 587)
        server.ehlo()
        server.starttls()
        server.login(email, password)

        

        msg = MIMEMultipart()
        msg['Subject'] = "Attendance Code"
        msg['To'] = receiver
        msg['From'] = email
        body = f"Hello {name}! Here is your attendence code. {text}"
        msg.attach(MIMEText(body))

        tobesend = msg.as_string()
        server.sendmail(email, receiver, tobesend)
        server.quit()


    def valuecompare():
        global code2
        global count 
        global message2
        code2 = str(entrybox.get())
        messageRL = Label(root5, text="wrong verification code! please try again", fg='red')

        if code2 != code:
            count = count -1
            messageRL.grid(row=5, column=0, columnspan=2)
            message2.config(text=f"Verification Attemp(s): {count}")
        if code == code2:
            root5.destroy()
            updatedatabase()

            #continue here
        if count == 0:
            count = 5
            message2.config(text= f"Verification Attemp(s): {count}")
            messageRL.config(text = "                                                                      ")
            messagebox.showwarning("WARNING", "You have used all your verification attemp! A new code will be sent to you, please use this new code to verify.")
            generate()

            
            
    def generate():
        global code
        a = string.ascii_letters
        b = string.digits
        letters = []
        for i in a:
            letters.append(i)
        for i in b:
            letters.append(i)

        code = random.choices(letters, k = 6)
        code = ''.join(code)
        sendcode(code)

    generate()
    #widgets
    root5 = Tk()
    authL = Label(root5, text = "AUTHENTHICATION", font=('arial', 25))
    message1 = Label(root5, text = "Please enter your code sent to your email:")
    message2 = Label(root5, text = f"Code Attemp(s): {count}")
    entrybox = Entry(root5, width = 40, borderwidth= 5)
    submitB = Button(root5, text = "Submit", width = 15, height= 5,command= valuecompare)

    authL.grid(row = 0, column = 0)
    message1.grid(row =1, column= 0)    
    message2.grid(row =2, column=0)
    entrybox.grid(row = 3 , columnspan = 2 )
    submitB.grid(row = 4, column = 0, columnspan= 2)

    
def facerecogg():
    global name
    # folder path
    dir_path = r'C:\\programming\\python\\CAS\\me'

    # list file and directories
    res = os.listdir(dir_path)
    name = ""
    for i in res:
        img = cv2.imread("C:\\Users\\molse\\OneDrive\\Dokumen\\GitHub\\CAS-face-recog\\image2.png") #image 1 to be compare, change the string varibale to ur pic file classide
        rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img_encoding = face_recognition.face_encodings(rgb_img)[0]


        img2 = cv2.imread(f"C:/programming/python/CAS/me/{i}")
        print("here1")
        rgb_img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2RGB) #image 2 to be compare, change string variable to ur 2nd pic file classide
        img_encoding2 = face_recognition.face_encodings(rgb_img2)[0]
        print("here2")

        result = face_recognition.compare_faces([img_encoding], img_encoding2)
        print(type(result[0]))
        if result[0] == True:
            print("Succesful")
            name = i.split(".png")
            name = name[0]
            break
    authentication()
        

def facecam():
    root3.destroy()
    root.destroy()
    infoo()
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
            #print("here")
            cv2.imwrite("image2.png", roi_grey) #string variable inside is the file classide of ur capture face
            root4.destroy()
            t2.kill()
            break
        root4.update()


    root4.mainloop()

    cap.release()
    cv2.destroyAllWindows()
    facerecogg()  


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
