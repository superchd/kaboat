from motor import *
#from socket import *
#from graphic import *
#from lidar import *
#from camera import *
from imu import *
import calculate as cal
import math
from gps import *
import rospy



def cmd_l(det):
    if -90 < det <=  -60:
        print("move Right 3")
        
    elif -60 < det <= -30:
        print("move Right 2")

    
    elif -30 < det <= 0:
        print("move Right 1")

    
    elif 0 < det <= 30:
        print("move Left 1")


    elif 30 < det <= 60:
        print("move Left 2")
    
    elif 60 < det < 90:
        print("move Left 3")
    

def cmd_r(det):
    if -90 < det <=  -60:
        print("move Left 3")
    
    elif -60 < det <= -30:
        print("move Left 2")
    
    elif -30 < det <= 0:
        print("move Left 1")

    elif 0 < det <= 30:
        print("move Right 1")

    elif 30 < det <= 60:
        print("move Right 2")

    elif 60 < det < 90:
        print("move Right 3")

class Lidarmotor:
    def __init__(self):
        if (0<= heading <= 90) and (0<= optimal <= 90) :
            
            if (heading<=optimal) :
                cmd_r(heading-optimal) # 배가 오른쪽으로 회전
            else :
                cmd_l(optimal-heading) # 배가 왼쪽으로 회전


        elif (0<= heading <= 90) and (270<= optimal <= 360):
            
                cmd_r(360 + (heading-optimal)) # 배가 오른쪽으로 회전


        elif (270<= heading <= 360) and (0<= optimal <= 90):

                cmd_l(360-(heading-optimal)) # 배가 왼쪽으로 회전

            
        elif (270<= heading <= 360) and (270<= optimal <= 360):
            
            if (heading<=optimal) :
                cmd_l(optimal-heading) # 배가 왼쪽으로 회전
            else :
                cmd_r(heading-optimal) # 배가 오른쪽으로 회전
