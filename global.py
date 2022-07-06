import rospy
from std_msgs.msg import Float64
import time
from motor import *
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
    if 0 < optimal <= 30:
        motor.motor_move(-10,15)
        print("left1")
    elif 30 < optimal <= 60:
        motor.motor_move(-20,15)
        print("left2")
    elif 60 < optimal < 90:
        motor.motor_move(-30,15)
        print("left3")

def cmd_r(optimal):
    if 0 < optimal <= 30:
        motor.motor_move(10,15)
        print("right1")
    elif 30 < optimal <= 60:
        motor.motor_move(20,15)
        print("right2")
    elif 60 < optimal < 90:
        motor.motor_move(30,15)
        print("right3")


def dozzy(optimal):
    global optimal2
    if 0 <= optimal2 <= 90:
        cmd_l(optimal2)

    elif 90 < optimal2 <= 180:
        cmd_r(optimal2-90)

if __name__ == '__main__':
    motor = Motor()
    while True:
        listener()
        time.sleep(1)
