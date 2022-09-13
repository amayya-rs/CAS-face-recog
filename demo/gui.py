from tkinter import *

root = Tk()
root2 = Tk()
root3 = Tk()

#all the canvases for the pages
canvas = Canvas(root, height=700, width=800)
canvas2 = Canvas(root2, height=700, width=800)
canvas3 = Canvas(root3, height=700, width=800)
canvas.pack()
canvas2.pack()
canvas3.pack()

#----------LOG IN PAGE-------

#name input widget
name1 = Label(root2, text="Enter your name:")
name1.place(relx=0.05, rely=0.38)
name = Entry(root2, width=50)
name.pack()
name.place(relx=0.5, rely=0.4, anchor=CENTER)

#class input widget
grade1 = Label(root2, text="Class:")
grade1.place(relx=0.05, rely=0.48)
grade_entry = Entry(root2, width=50)
grade_entry.pack()
grade_entry.place(relx=0.5, rely=0.5, anchor=CENTER)

#email input widget
email = Label(root2, text="Email ID:")
email.place(relx=0.05, rely=0.58)
email_entry = Entry(root2, width=50)
email_entry.pack()
email_entry.place(relx=0.5, rely=0.6, anchor=CENTER)

#continue button 
continue_button = Button(root2, text="Continue")
continue_button.place(relx=0.5, rely=0.7, anchor=CENTER)

#----------MAIN PAGE---------------------
fingerprint = Button(root, text="Fingerprint", padx=30, pady=30)
fingerprint.place(relx=0.1, rely=0.4)

face_id = Button(root, text="Face Recognition and OTP", padx=20, pady=20)
face_id.place(relx=0.4, rely=0.4)

qr_code = Button(root, text="QR Code", padx=30, pady=30)
qr_code.place(relx=0.8, rely=0.4)


#----------FACE RECOGNITION PAGE----------

#face cam activation screen
button = Button(root3, text="Click to activate camera", padx=50, pady=50)
button.place(relx=0.5, rely=0.5, anchor=CENTER)



root.mainloop()
root2.mainloop()
root3.mainloop()
