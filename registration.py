import tkinter as tk
from tkinter import ttk
import PIL.Image as Image
import PIL.ImageTk as ImageTk
import cv2
import cognitive_face as CF
import numpy as np

KEY = 'd134dc82f5f14600a36f20161ecd395f'
CF.Key.set(KEY)

BASE_URL = 'https://westcentralus.api.cognitive.microsoft.com/face/v1.0/'
CF.BaseUrl.set(BASE_URL)

imgUrl = 'https://raw.githubusercontent.com/Microsoft/Cognitive-Face-Windows/master/Data/detection1.jpg'
groupId = str("1")

#Set up GUI
window = tk.Tk()
window.wm_title("Face Registration")
window.config(background="#FFFFFF")

#Set up the camera
cameraWidth = 600
cameraHeight = 500
camera = cv2.VideoCapture(0)
camera.set(3, cameraWidth) # set video width
camera.set(4, cameraHeight) # set video height
face_detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
minW = 0.1 * camera.get(3)
minH = 0.1 * camera.get(4)
grayCapturedImage = None

#Graphics window
imageFrame = tk.Frame(window, width= cameraWidth, height= cameraHeight)
imageFrame.grid(row = 3, column = 0, padx = 10, pady = 2)

#Capture video frames
lmain = tk.Label(imageFrame)
lmain.grid(row=3, column=0)

#Get the user name
userNameFrame = tk.Frame(window)
userNameFrame.grid(row = 0, column = 0, padx = 10, pady = 2, sticky = "W")

userName = tk.StringVar(None)
userNameLabel = tk.Label(userNameFrame, text = "Name")
userNameLabel.grid(row = 0, column = 0)
userNameEntry = tk.Entry(userNameFrame, textvariable = userName)
userNameEntry.grid(row = 0, column  = 1)

#Display the user
errorString = tk.StringVar(None)
errorLabel = tk.Label(window, textvariable = errorString)
errorLabel.grid(row = cameraWidth + 5, column = 0, padx = 10, pady = 2)



def takeSnapShot():

    global  grayCapturedImage
    errorString.set("")
    cv2.imwrite('registration.jpg', grayCapturedImage)
    if userName.get() != "":
        face_detection_result = CF.face.detect("C:\\Users\\PVallabh\\Desktop\\face recognition azure\\registration.jpg")
        if face_detection_result != []:
            personCreatedResponse = CF.person.create("1", userName.get())
            personId = personCreatedResponse['personId']
            addFaceResponse = CF.person.add_face("C:\\Users\\PVallabh\\Desktop\\face recognition azure\\registration.jpg", groupId, personId)
            trainingResponse = CF.person_group.train(groupId)
            errorString.set("Information is added")
        else:
            errorString.set("No face is detected in the image taken")
    else:
        errorString.set("Enter your name")

def show_frame():

    global grayCapturedImage
    _, frame = camera.read()
    frame = cv2.flip(frame, 1)
    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
    grayCapturedImage = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_detector.detectMultiScale(
        grayCapturedImage,
        scaleFactor = 1.2,
        minNeighbors = 5,
        minSize=(int(minW), int(minH)),
    )

    for(x,y,w,h) in faces:
        cv2.rectangle(cv2image, (x,y), (x+w,y+h), (0,255,0), 2)
    img = Image.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image = img)
    lmain.imgtk = imgtk
    lmain.configure(image = imgtk)
    lmain.after(10, show_frame)

#Button to capture the photo
button = tk.Button(window, text = "Capture", command = takeSnapShot)
button.grid(row = cameraWidth + 3, column = 0, padx = 10, pady = 2)
show_frame()
window.mainloop()