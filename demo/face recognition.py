import cv2
import face_recognition

#this is a face recognition pg, it will compare two pics and tell whether the face in the 2 pics are similar

img = cv2.imread("image.png") #image 1 to be compare, change the string varibale to ur pic file classide
rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
img_encoding = face_recognition.face_encodings(rgb_img)[0]


img2 = cv2.imread("C:/programming/python/CAS/me/Screenshot 2022-08-16 213149.png")
rgb_img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2RGB) #image 2 to be compare, change string variable to ur 2nd pic file classide
img_encoding2 = face_recognition.face_encodings(rgb_img2)[0]

result = face_recognition.compare_faces([img_encoding], img_encoding2)
print("result: ", result)


cv2.imshow("Img", img)
cv2.imshow("Img 2", img2)
cv2.waitKey(0)