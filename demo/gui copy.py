from tkinter import *
from tkinter import messagebox
import mysql.connector
import threading
import sys

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

exit1 = ''

def inputcheck():

    global exit1
    global loginbutton
    global root2
    global classidE
    global passwordE
    while True:
        lock.acquire()

        if exit1 == True:
            root2.destroy()
            
        if exit1 != True:
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
    global exit1
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
        exit1 = True
        main()

    

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
    
#----------MAIN PAGE---------------------
    #Canvas and page settings
    root = Tk()
    canvas = Canvas(root, height=700, width=800)
    canvas.pack()
    #

    classlabel = Label(root, text = f"Hello {Class}")

    fingerprint = Button(root, text="Fingerprint", padx=30, pady=30)
    fingerprint.place(relx=0.1, rely=0.4)

    face_id = Button(root, text="Face Recognition and OTP", padx=20, pady=20)
    face_id.place(relx=0.4, rely=0.4)

    qr_code = Button(root, text="QR Code", padx=30, pady=30)
    qr_code.place(relx=0.8, rely=0.4)

    root.mainloop()


def face():
    #canvas and page setting
    root3 = Tk()
    canvas3 = Canvas(root3, height=700, width=800)
    canvas3.pack()

#----------FACE RECOGNITION PAGE----------

#face cam activation screen
    button = Button(root3, text="Click to activate camera", padx=50, pady=50)
    button.place(relx=0.5, rely=0.5, anchor=CENTER)

    root3.mainloop()


#threading
lock = threading.Lock()
if __name__ == "__main__" :
    first = threading.Thread ( target = loginpage ) 
    second = threading.Thread ( target = inputcheck ) 
    first.start() 
    second.start() 
    first.join()
    second.join()





#loginpage()

#main()
#face()
