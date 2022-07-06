import smbus
import math


class Imu:

    __scales = {
        0.88: [0, 0.73],
        1.30: [1, 0.92],
        1.90: [2, 1.22],
        2.50: [3, 1.52],
        4.00: [4, 2.27],
        4.70: [5, 2.56],
        5.60: [6, 3.03],
        8.10: [7, 4.35],
    }

    # 초기화
    def __init__(self, port=1, address=0x1E, gauss=4.7, declination=(-2, 5)):
        print("Imu init")
        self.bus = smbus.SMBus(port)
        self.address = address

        (degrees, minutes) = declination
        self.__declDegrees = degrees
        self.__declMinutes = minutes
        self.__declination = (degrees + minutes / 60) * math.pi / 180

        (reg, self.__scale) = self.__scales[gauss]
        self.bus.write_byte_data(self.address, 0x00, 0x70)
        self.bus.write_byte_data(self.address, 0x01, reg << 5)
        self.bus.write_byte_data(self.address, 0x02, 0x00)

    def declination(self):
        return self.__declDegrees, self.__declMinutes

    def twos_complement(self, val, len):
        if val & (1 << len - 1):
            val = val - (1 << len)
        return val

    def __convert(self, data, offset):
        val = self.twos_complement(data[offset] << 8 | data[offset+1], 16)
        if val == -4096: return None
        return round(val * self.__scale, 4)

    def axes(self):
        data = self.bus.read_i2c_block_data(self.address, 0x00)
        x = self.__convert(data, 3)
        y = self.__convert(data, 7)
        z = self.__convert(data, 5)
        return x, y, z

    def heading(self):
        (x, y, z) = self.axes()
        headingRad = math.atan2(y, x)
        headingRad += self.__declination

        if headingRad < 0:
            headingRad += 2 * math.pi

        elif headingRad > 2 * math.pi:
            headingRad -= 2 * math.pi

        headingDeg = headingRad * 180 / math.pi
        return headingDeg

    def degrees(self, headingDeg):
        degrees = math.floor(headingDeg)
        minutes = round((headingDeg - degrees) * 60)
        return degrees, minutes

    def imu_read(self):
        imu_data = self.degrees(self.heading())[0]
        return imu_data

    def __str__(self):
        (x, y, z) = self.axes()
        return "Axis X: " + str(x) + "\n" \
               "Axis Y: " + str(y) + "\n" \
               "Axis Z: " + str(z) + "\n" \
               "Declination: " + self.degrees(self.declination()) + "\n" \
               "Heading: " + self.degrees(self.heading()) + "\n"
