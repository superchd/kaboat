import rospy
from std_msgs.msg import Float64
import time
from double_motor import *
from socket import *
import calculate as cal
optimal2 = 0

def callback(msg):
    global optimal2
    optimal2 = msg.data

def listener():
    rospy.init_node('optimal_subscriber_node', anonymous=True)
    rospy.Subscriber("optimal_angle", Float64, callback)
    print(optimal2)
    dozzy(optimal2)
    


def cmd_l(optimal):
    if 10 < optimal <= 30:
        motor.motor_move(-27,-39)
        print("left1")
    elif 30 < optimal <= 60:
        motor.motor_move(-22.5,-32.5)
        print("left2")
    elif 60 < optimal <= 90:
        motor.motor_move(-25.5,-30.5)
        print("left3")
    elif 0 < optimal <= 10:
        motor.motor_move(-30, -30)
        print("go straight")


def cmd_r(optimal):
    if 0 < optimal <= 30:
        motor.motor_move(-39,-27)
        print("right1")
    elif 30 < optimal <= 60:
        motor.motor_move(-32.5,-22.5)
        print("right2")
    elif 60 < optimal <= 80:
        motor.motor_move(-30.5,-25.5)
        print("right3")
    elif optimal == 0 or 80 < optimal <= 90:
        motor.motor_move(-30,-30)
        print("go straight")
    
    


def dozzy(optimal):
    global optimal2
    if 0 < optimal2 <= 90:
        cmd_r(optimal2)

    elif 90 < optimal2 <= 180:
        cmd_l(optimal2 - 90)

if __name__ == '__main__':
    motor = Motor()
    while True:
        listener()
        time.sleep(0.5)
