#import libraries
import numpy as np
import cv2
import time
#video capture object with 0th webcam 
cap = cv2.VideoCapture(0)
#to adjust camera according to env
time.sleep(2)
background = 0
#to get proper image of backgrownd before running in ret object
for i in range(30):
  ret,background = cap.read()
#run while loop content till image is capturing 
while(cap.isOpened()):
  #captuer image seperately
  ret, img = cap.read()
  if not ret:
    break
  #BGR : Blue, Green, Red; HSV: Hue Saturation Value
  hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
  #color saturation uses 360 angles for color but in opencv we
  #have only 8 bits to store color value 2^8 = 255 ;
  #hence we cannot store color value having angle greater than 255 
  #HSV values 
  lower_red = np.array([0,120,70])
  upper_red = np.array([10,255,255])
  #seperating cloak part
  mask1 = cv2.inRange(hsv, lower_red, upper_red)
  lower_red = np.array([170,120,70])
  upper_red = np.array([180,255,255])
  mask2 = cv2.inRange(hsv, lower_red, upper_red)

  mask1 = mask1 + mask2
  #to remove noise
  mask1 = cv2.morphologyEx(mask1, cv2.MORPH_OPEN, np.ones((3,3),np.uint8),iterations = 2)
  #to increase smoothness
  mask1 = cv2.morphologyEx(mask1, cv2.MORPH_DILATE, np.ones((3,3),np.uint8),iterations = 1)
  #mask2 will hold part other than cloak
  mask2 = cv2.bitwise_not(mask1)
  #for segmentation of color
  res1 = cv2.bitwise_and(background, background, mask= mask1)
  #substitute clpak part
  res2 = cv2.bitwise_and(img,img, mask=mask2)

  final_output = cv2.addWeighted(res1, 1, res2, 1, 0)
  cv2.imshow('well !', final_output)
  k = cv2.waitKey(10)
  if k == 27:
    break
cap.release()
cv2.destroyAllWindows()

