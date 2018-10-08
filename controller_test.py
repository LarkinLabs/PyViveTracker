import triad_openvr
import time
import sys
import cv2
import numpy as np
import csv
from time import gmtime, strftime
v = triad_openvr.triad_openvr()
v.print_discovered_objects()

if len(sys.argv) == 1:
    interval = 1/5
elif len(sys.argv) == 2:
    interval = 1/float(sys.argv[0])
else:
    print("Invalid number of arguments")
    interval = True
xoffset=0
yoffset=0
zoffset=0
 # Create a black image
img = np.zeros((512,512,3), np.uint8)
x=0
y=0
z=0
pos = []
while(True):
    start = time.time()
    txt = ""
    for each in v.devices["controller_1"].get_pose_euler():
        txt += "%.4f" % each
        txt += ","
    mylist = txt.split(',')
    if xoffset == 0:
        xoffset=float(mylist[0])
        yoffset=float(mylist[1])
        zoffset=float(mylist[2])
    x =int((float(mylist[0])-xoffset)*1000)
    y= int((float(mylist[1])-yoffset)*1000)
    z=int((float(mylist[2])-zoffset)*1000)
    pos.append((x,y,z))
    print(x,y, z)
    cv2.circle(img,(256+(x/500),256+(z/500)), 1, (0,0,255), -1)
               
    cv2.imshow('image',img)
    k= cv2.waitKey(10)
    if k == 27:         # wait for ESC key to exit
        cv2.destroyAllWindows()
        csvfile = strftime("%Y-%m-%d-%H-%M.csv", gmtime())
        with open(csvfile, "w") as output:
            writer = csv.writer(output, lineterminator='\n')
            writer.writerows(pos)
        break 
        
    #time.sleep(.1)
