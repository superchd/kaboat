from double_motor import*

if __name__ == "__main__":


    motor = Motor()

        motor.motor_move(-10,-10)
        time.sleep(6)

        motor.motor_move(-15,-10) ##1번
        time.sleep(1)
        
        motor.motor_move(
        # motor.motor_move(30,0)

       # time.sleep(8)
       # motor.motor_move(30,-30)

       # time.sleep(18)

        del motor

