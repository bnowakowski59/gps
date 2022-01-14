# !/usr/bin/env python3

import adafruit_mpu6050
import board

from math import sqrt, atan2, degrees
from time import sleep

from raspberry_hat.config import *


class MultiPurposeUnit:
    """
    MPU6050
    """

    def __init__(self, timeout):
        self.i2c = board.I2C()
        self.mpu = adafruit_mpu6050.MPU6050(self.i2c)
        self.timeout = timeout

    def get_timeout(self):
        sleep(self.timeout)

    def get_inclinometer(self):
        x, y, z = self.mpu.acceleration

        def vector_2_degrees(x, y):
            angle = degrees(atan2(y, x))
            # if angle < 0:
            #     angle += 360
            return angle

        return vector_2_degrees(x, z), vector_2_degrees(y, z)

    def get_accelerometer(self):
        #  Ensure that we are not sleeping or cycle wont work.
        self.mpu.sleep = False

        #  Set a slow cycle rate.
        self.mpu.cycle_Rate = adafruit_mpu6050.Rate.CYCLE_1_25_HZ

        #  Enable cycle mode
        self.mpu.cycle = True

        #  Get acceleration while standing.
        acceleration = abs(sqrt(self.mpu.acceleration[0] ** 2 +
                                self.mpu.acceleration[1] ** 2 +
                                self.mpu.acceleration[2] ** 2))

        self.mpu.cycle = False
        self.mpu.sleep = True

        return acceleration


def checkMPU():
    mpu = MultiPurposeUnit(timeout_mpu)
    sleep_measure_acceleration = mpu.get_accelerometer()
    sleep_measure_inclinometer = mpu.get_inclinometer()

    while True:
        acceleration = mpu.get_accelerometer()
        angle_xz, angle_yz = mpu.get_inclinometer()
        print(f'xz: {angle_xz} yz: {angle_yz}')
        print(f'acc: {acceleration}')
        rotate_xz = abs(sleep_measure_inclinometer[0] - angle_xz)
        rotate_yz = abs(sleep_measure_inclinometer[1] - angle_yz)

        #  If inclinometer weill show  higher value  than above, device will
        #  power on and send sms if True.
        if rotate_yz <= 90 and rotate_xz <= 90:
            #  If accelerometer will show higher value than above, device will
            #  power on and send sms if True.
            if abs(sleep_measure_acceleration - acceleration) <= 1:
                mpu.get_timeout()
                continue
            else:
                print('Vehicle movement detected')
                sleep(1)

                return 'Vehicle movement detected', True

        else:
            print('Device rotation detected')
            sleep(1)
            return 'Device rotation detected', True
