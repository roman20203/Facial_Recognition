
import cv2
#imports opencv 

from deepface import DeepFace
#imports deepface

from person import *

import glob

"""
img = cv2.imread('images/ben/reference_ben.jpeg',-1)

cv2.imshow('Image of Ben',img)
cv2.waitKey(0)
cv2.destroyAllWindows()
"""



ben_obj = Person("ben")


print(ben_obj.giveDirectory())
print(ben_obj.giveName())
print(ben_obj.giveImg())
