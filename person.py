import threading
#threading allows for multiple tasks to be run at the same time, important when using external softwares

import cv2
#imports opencv 

from deepface import DeepFace
#imports deepface

class Person: 

    def __init__(self, name): 
        self.name = name
        self.ref = "reference_" + name
        self.directory = 'images/' + self.name + '/' + self.ref + ".jpeg"
        self.img = cv2.imread(self.directory,-1)
        

    def giveName(self): 
        return self.name
    def giveReferencefile(self): 
        return self.ref
    def giveDirectory(self): 
        return self.directory
    def giveImg(self): 
        img = cv2.imread(self.directory,-1)
        return cv2.flip(img,1)
    

    


