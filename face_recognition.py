import tkinter as tk
import PIL.Image as Image
import PIL.ImageTk as ImageTk
import cv2
import cognitive_face as CF
import time
from tkinter import ttk
import numpy as np

KEY = 'd134dc82f5f14600a36f20161ecd395f'  
CF.Key.set(KEY)

BASE_URL = 'https://westcentralus.api.cognitive.microsoft.com/face/v1.0/'
CF.BaseUrl.set(BASE_URL)

img_url = 'https://raw.githubusercontent.com/Microsoft/Cognitive-Face-Windows/master/Data/detection1.jpg'

group_id = str("1")


#Set up GUI
window = tk.Tk()
window.wm_title("Face Recognition")
window.config(background="#FFFFFF")

#Graphics window
imageFrame = tk.Frame(window, width=600, height=500)
imageFrame.grid(row=0, column=0, padx=10, pady=2)

#Capture video frames
lmain = tk.Label(imageFrame)
lmain.grid(row=0, column=0)

#Display the user
identifyString = tk.StringVar()
identifyLabel = tk.Label(window,textvariable=identifyString)
identifyLabel.grid(row = 602, column=0, padx=10, pady=2)
cap = cv2.VideoCapture(0)
cap.set(3, 600) 
cap.set(4, 500) 
face_detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
minW = 0.1*cap.get(3)
minH = 0.1*cap.get(4)
gray = None

def takeSnapShot():
    global  gray
    found_user = ""
    cv2.imwrite('face_detect.jpg', gray)
    face_detection_result = CF.face.detect("C:\\Users\\PVallabh\\Desktop\\face recognition azure\\face_detect.jpg")
    print(face_detection_result)
    if face_detection_result != []:
        face_ids = []

        for number_of_faces_detected in range(0, len(face_detection_result)):
            face_ids.append(face_detection_result[number_of_faces_detected]['faceId'])

        face_identify_result = CF.face.identify(face_ids, group_id)

        if face_identify_result != []:
            for identified_face in range(0, len(face_identify_result)):
                face_candidates = face_identify_result[identified_face]['candidates']

                if face_candidates != []:
                    for candidate in range(0, len(face_candidates)):
                        person_name = CF.person.get(group_id, str(face_candidates[candidate]['personId']))
                        print(person_name['name'])
                        found_user = person_name['name']
                        #identifyString.set(person_name['name'])
                else:
                    if found_user == "":
                        found_user = "Unknown user"

            identifyString.set(found_user)

        print(face_identify_result)

def show_frame():
    global gray
    _, frame = cap.read()
    frame = cv2.flip(frame, 1)
    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_detector.detectMultiScale(
        gray,
        scaleFactor=1.2,
        minNeighbors=5,
        minSize=(int(minW), int(minH)),
    )

    for(x,y,w,h) in faces:
        cv2.rectangle(cv2image, (x,y), (x+w,y+h), (0,255,0), 2)
    img = Image.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image=img)
    lmain.imgtk = imgtk
    lmain.configure(image=imgtk)
    lmain.after(10, show_frame)


button = tk.Button(window,text = "Capture",command = takeSnapShot)
button.grid(row = 600, column=0, padx=10, pady=2)
show_frame()
window.mainloop()