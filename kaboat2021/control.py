from double_motor import *
#from socket import *
#from graphic import *
#from lidar import *
#from camera import *
from imu import *
import calculate as cal
import math
from gps import *

# 실제 부표 크기(cm)
REAL_BUOY_SIZE = 100

def waypoint_step(self, waypoints, error_distance, tolerance):
    if self.i + 1 != len(waypoints):
        if error_distance > tolerance:
            waypoint = waypoints[self.i]
        elif error_distance <= tolerance:
            waypoint = waypoints[self.i + 1]
            self.i = self.i + 1
    elif self.i + 1 == len(waypoints):
        waypoint = waypoints[self.i]

    return waypoint

# mode1 : 사용자가 직접 조종
class ControlMode1:
    # 초기화
    def __init__(self, joy_stick):
        print("ControlMode1 init")

        # 모터
        self.motor = Motor()

        # 모터 기본 셋팅값
        self.speed = 20
        self.degree = 40
        self.direction = 0

        # 소켓 통신 셋팅
        self.sock = socket(AF_INET, SOCK_STREAM)
        self.sock.bind(('', 1972))
        self.sock.listen(1)

        # 조이스틱 사용 여부
        self.joy_stick = joy_stick

    # 직접 주행 시작
    def drive_myself(self):
        # 소켓 통신 시작
        conn, _ = self.sock.accept()

        # 종료 버튼 입력까지 반복
        while True:
            try:
                # 소켓 통신으로 데이터 받아오기
                data = conn.recv(1024).decode('utf-8')

                # 조이스틱을 사용할 때
                if self.joy_stick:
                    if data != '':
                        conn.send("ok".encode('utf-8'))
                        self.motor.motor_move(int(data[0:3]), int(data[3:6]))

                # 조이스틱을 사용하지 않을 때
                else:
                    if data == "exit":
                        break
                    if data == "up":
                        self.direction = 1
                        self.motor.motor_move_only_speed(self.direction * self.speed)
                    elif data == "down":
                        self.direction = -1
                        self.motor.motor_move_only_speed(self.direction * self.speed)
                    elif data == "left":
                        self.direction = -1
                        self.motor.motor_move_only_degree(self.direction * self.degree)
                    elif data == "right":
                        self.direction = 1
                        self.motor.motor_move_only_degree(self.direction * self.degree)
                    elif data == "keyupbldc":
                        self.motor.motor_move_only_speed(0)
                    elif data == "keyupservo":
                        self.motor.motor_move_only_degree(0)
                    if data == "one":
                        self.speed = 15
                        self.motor.motor_move_only_speed(self.direction * self.speed)
                    elif data == "two":
                        self.speed = 25
                        self.motor.motor_move_only_speed(self.direction * self.speed)
                    elif data == "thr":
                        self.speed = 35
                        self.motor.motor_move_only_speed(self.direction * self.speed)
                    elif data == "for":
                        self.speed = 45
                        self.motor.motor_move_only_speed(self.direction * self.speed)
                    elif data == "fiv":
                        self.speed = 55
                        self.motor.motor_move_only_speed(self.direction * self.speed)
            # 오류 발생
            except error as err:
                print("오류 발생 : " + err)
                break

    # 종료
    def __del__(self):
        print("ControlMode1 del")
        del self.motor
        del self.sock


# mode2 : camera + lidar 사용해서 자율 주행
class ControlMode2:
    # 초기화
    def __init__(self):
        print("ControlMode2 init")

        # 모터 생성 및 기본값 설정
        self.motor = Motor()
        self.speed = 15
        self.i = 0 #for 'Waypoints List' Index
        self.error_Distance = 0.00001 # if error_distance = 0
        self.imu = Imu()

    def look_forward(self):
        self.forward_direction = self.imu.imu_read()

        while (0 <= self.forward_direction < 7 or 136 <= self.forward_direction <= 360 ):
            self.motor.motor_move(0,20)
            time.sleep(1)

    def look_backward(self):
        self.forward_direction = self.imu.imu_read()
        while (7 <= self.forward_direction < 136 ):
            self.motor.motor_move(0,20)
            time.sleep(1)

    def move_to_destination(self, waypoint):
        del_lati, del_longi = location(waypoint)
        del_longi = del_longi * 100000
        print(del_longi)
        tolerance = math.sqrt(math.pow(del_lati , 2) + math.pow(del_longi,2))
       #time.sleep(3)
        self.forward_direction = self.imu.imu_read()
        if (0):
            print("Go straight")
            self.motor.motor_move(0, 30)
            time.sleep(2)
        else :
            if (del_longi >= 0.1):
                print("Left")
                self.motor.motor_move(-15, -25)
                time.sleep(2)
            elif (del_longi < -0.1):
                print("Right")
                self.motor.motor_move(-25,-15)
                time.sleep(2)
            else :
                print("Go straight2")
                self.motor.motor_move(-20, -20)

    def move_to_home(self, waypoint):
        del_lati, del_longi = location(waypoint)
        del_longi = del_longi * 100000
        print("%f.6", del_longi)
        tolerance = math.sqrt(math.pow(del_lati , 2) + math.pow(del_longi,2))
        self.forward_direction = self.imu.imu_read()
        if (0):
            print("Go straight")
            self.motor.motor_move(-20,-20)
            time.sleep(2)
        else :
            if (del_longi >= 0.1):
                print("Right_home")
                self.motor.motor_move(-25, -15)
                time.sleep(2)
            elif (del_longi < -0.1):
                print("Left_home")
                self.motor.motor_move(-15,-25)
                time.sleep(2)
            else :
                print("Go straight2_home")
                self.motor.motor_move(-20, -20)

    #def __del__(self):
    #   pass