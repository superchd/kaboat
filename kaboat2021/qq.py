from imu import *

imu = Imu()

while True:
    forward_direction = imu.imu_read()
    print(forward_direction)

