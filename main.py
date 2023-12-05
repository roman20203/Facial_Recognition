import threading
#threading allows for multiple tasks to be run at the same time, important when using external softwares

#glob.glob will allow me to find files and directories which will be used to find the names of people in database
import glob

#imports opencv 
import cv2

#imports deepface
from deepface import DeepFace

from person import *





#Creates object for the camera that will be used 
#number represents which camera to use , 0, is my iphone, 1 is the laptop camera
capture = cv2.VideoCapture(1)


#Sets width of camera frame
capture.set(cv2.CAP_PROP_FRAME_WIDTH, 500)
#sets Height of camera frame
capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 400)



#will keep track of people who already have objects so more arent created
#should be toto,coco,ben
names_of_existing_obj = []
#list of objects
created_objects = {}
detected_name = ""
"""
Uses glob.glob to find the people in the folder and create a list of names based on who is added into the database
"""
def people_in_database(): 
    people_directory  = glob.glob('images/*/')

    people_name = []

    for i in people_directory: 
        name = i[7:-1]
        people_name.append(str(name))
        
    return people_name

def Person_Obj_Creator(): 
    for person in (people_in_database()):
        if person not in names_of_existing_obj: 
            created_objects[person] = Person(person) 
            names_of_existing_obj.append(person)
        
Person_Obj_Creator()
# this is how you access the objects using a name string ->> print(created_objects["name"])

#ben_img = created_objects["ben"].giveImg()



face_match = False




def face_check(frame,name): 
    global face_match 
    global detected_name
    print(name +" is sent")
    face_img = created_objects[str(name)].giveImg()
    result = DeepFace.verify(frame, face_img.copy(), enforce_detection= False)["verified"]
    #enforce_detection= False
    

    #Checks for a new face if there is we assign detected_name if not we then check if the previously detected face is still there 
     #if the previously detected face is not there 
    if result:
        face_match = True 
        detected_name =str(name)
        print(detected_name+" is detected")
            
        #tests if previously detected face is still in frame if so it will keep them as the detected name

    elif not result and detected_name != "" and detected_name != name: 

        temp_img = created_objects[str(detected_name)].giveImg()

        if (DeepFace.verify(frame, temp_img.copy(), enforce_detection= False))["verified"]:
            face_match = True
            print(detected_name +" is RE detected")
        else:
            face_match = False
            print(detected_name+" is not being RE detected")
            detected_name = ""
    else: 
        face_match = False
        print(name + " is NOT detected")
            
    #except ValueError as e: 
        #print(f"ValueError: {e}")
        #face_match = False




#will have to return boolean for match, and string for name

"""
def face_check(frame): 
    global face_match 

    try: 
        if (DeepFace.verify(frame, ben_img.copy(), enforce_detection= False))["verified"]:
            face_match = True 
        else: 
            face_match = False
            
    except ValueError as e: 
        print(f"ValueError: {e}")
        face_match = False
        
"""

counter = 0

#Create infinite loop that will continuosly read frames


while True: 
    #captures the frame 
    #read() returns a boolean(return_) and Data (frame)
    exists, pre_frame = capture.read()
    
    frame= cv2.flip(pre_frame,1)
    if exists: 
        if counter % 60 == 0:

            threads = []

            for count in range(len(names_of_existing_obj)):
                name = names_of_existing_obj[count]
                try:
                    # Create a thread for each person
                    thread = threading.Thread(target=face_check, args=(frame.copy(), str(name)))
                    threads.append(thread)
                    thread.start()
                    print(count)
                except ValueError:
                    pass

            # Wait for all threads to finish
            for thread in threads:
                thread.join()


            """
            for count in range(len(names_of_existing_obj)): 
                name = names_of_existing_obj[count]

                try: 
                    face_check(frame.copy(),str(name))
                    #threading.Thread(target=face_check, args=(frame.copy(),str(name),)).start()
                    print(count)
                except ValueError: 
                    pass
            """

        counter +=1

        if face_match: 
            cv2.putText(frame,"Hello " + detected_name,(20,450),cv2.FONT_HERSHEY_SIMPLEX, 2,(0, 255, 0),3)
        else: 
            cv2.putText(frame,"Hello Stranger",(20,450),cv2.FONT_HERSHEY_SIMPLEX, 2,(0, 0, 255),3)

        #show the frame 
        #imshow("window_name", image)
        cv2.imshow("Display",frame)

    key = cv2.waitKey(1)
    if key == ord("q"):
        break
        

#now we want to close the window 
capture.release()
cv2.destroyAllWindows()

