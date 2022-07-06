#!/usr/bin/env python
# -*- coding: utf-8 -*-
from double_motor import *
from control import *
from gps import *
# ################### MODE LIST ####################
# mode1 : 사용자가 직접 조종
# mode2 : camera + lidar 사용해서 자율 주행
# ##################################################

# 메인 함수(프로그램 실행)
if __name__ == "__main__":
    # 모드 입력
    #mode = int(input("어떤 모드를 실행할까요?(1: 직접 조종, 2: 카메라+라이다)\n"))
    #print("write coordinate, write start point and end point")
    #n,m=map(int, input().split())
    #revised=[0 for _ in range(n)]

    #for i in range(n):
    #    revised[i]=list(map(float, input().split()))
    mode = 2
    # mode1(직접 주행일 때)
    if mode == 1:
        # 클래스 불러오기
        control = ControlMode1(True)

        # 주행 시작
        control.drive_myself()

    # mode2(camera + lidar)
    elif mode == 2:
        # 클래스 불러오기
        control = ControlMode2()

       
        waypoints = [(35.16088867,128.736281), (35.1794436, 128.7285156), (35.18139648, 128.734375), (35.16357422, 128.7421875)]
        waypoint = waypoints[0]
        print("I will tell you waypoints")
        print(*waypoints, sep = '\n')
        print("\n")
        del_lati, del_longi = location(waypoint)
        error_distance = math.sqrt(math.pow(del_lati , 2) + math.pow(del_longi,2)) 
        tolerance = 205.078
        i = 0
        change = 0

        
        # 주행 시작
        while True:
            x_diff, y_diff = location(waypoint)
            if (x_diff < 0):
                if (change == 0):
                    control.move_to_destination(waypoint)
                elif (change == 2):
                    control.look_forward()
                    control.move_to_destination(waypoint)

            else :
                if (change == 1):
                    control.look_backward()
                    control.move_to_destination(waypoint)
                elif (change == 3):
                    control.look_backward()
                    control.move_to_destination(waypoint)

            error_distance = math.pow(10, 5) * math.sqrt(math.pow(x_diff , 2) + math.pow(y_diff,2))
            
            if x_diff != 0 and y_diff != 0:
                if i + 1 != len(waypoints):
                    if error_distance > tolerance:
                        print("i + 1 != len(waypoints), and error_distance > tolerance\n")
                        waypoint = waypoints[i]
                    elif error_distance <= tolerance:
                        waypoint = waypoints[i + 1]
                        print("i + 1 != len(waypoints), and error_distance <= tolerance\n")
                        break
                        i = i + 1
                elif i + 1 == len(waypoints) + 1:
                    print("Let's break\n")
                    break

    del control