from double_motor import *

# 메인 함수(프로그램 실행)
if __name__ == "__main__":
    # 모드 입력
    # mode = int(input("어떤 모드를 실행할까요?(1: 직접 조종, 2: 카메라+라이다)\n"))
    mode = 2

    # mode1(직접 주행일 때)
    if mode == 1:
        # 클래스 불러오기
        control = ControlMode1(True)

        # 주행 시작
        control.drive_myself()

    # mode2(camera + lidar)
    elif mode == 2:
        motor = Motor()
        a = 30
        s = 30
    
        motor.motor_move(0,0)
        time.sleep(15)
        motor.motor_move(0,0)
        time.sleep(4)
        motor.motor_move(-30,0)
        time.sleep(4)
        motor.motor_move(-80,-80)
        time.sleep(3)
        motor.motor_move(0,0)
        time.sleep(100)
        motor.motor_move(-30,-28)
        time.sleep(3)
        motor.motor_move(-30,-30)
        time.sleep(8)
        motor.motor_move(0,0)
        time.sleep(1)
        motor.motor_move(0,-30)
        time.sleep(3)
        motor.motor_move(-30,-30)
        time.sleep(5)
        motor.motor_move(0,-30)
        time.sleep(3)
        motor.motor_move(0,0)
        time.sleep(3)
        motor.motor_move(-30,-30)
        time.sleep(10)
        
        motor.motor_move(0,0)
        time.sleep(1)
        motor.motor_move(0,-30)
        time.sleep(6)
        motor.motor_move(0,0)
        time.sleep(1)
        motor.motor_move(-30,-30)
        time.sleep(2)
        motor.motor_move(-30,-28)
        time.sleep(8)
        motor.motor_move(0,0)
        time.sleep(2)
        motor.motor_move(0,-30)
        time.sleep(6)
        motor.motor_move(0,0)
        time.sleep(2)
        motor.motor_move(-30,-28)
        time.sleep(20)


        # motor.motor_move(30,0)

       # time.sleep(8)
       # motor.motor_move(30,-30)

       # time.sleep(18)
 
        del motor

