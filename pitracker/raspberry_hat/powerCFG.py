from raspberry_hat.gps_gnss_gprs_hat import *

from time import sleep
from raspberry_hat.config import *

import RPi.GPIO as GPIO
import serial


class SerialPort:

    @staticmethod
    def open():
        """
        Opening  UART serial port to GPRS/GNSS Hat module form Raspberrypi.
        """
        ser = serial.Serial(PORT,
                            baudrate=115200,
                            bytesize=serial.EIGHTBITS,
                            parity=serial.PARITY_NONE,
                            stopbits=serial.STOPBITS_ONE,
                            timeout=1
                            )
        return ser

    @staticmethod
    def close():
        pass


class PowerCFG:
    
    def __init__(self, ser, send_sms):
        self.ser = ser
        self.send_sms = send_sms

    def boot_on(self):
        """
        Connect to the modem and configure it in an
        attempt to standardize the behavior of the
        many vendors and models.
        """

        #  Closing GPRS connection if open.
        if GPRS().closeConnection():
            sleep(1)

        while True:

            #  Print UART connection status True or False
            if self.ser.isOpen():
                print(f"UART connection - {self.ser.isOpen()}")

            #  Send AT command to check if there is coomunication with board.
            sleep(5)
            answer = (send_at('AT', 'OK', 1, self.ser))

            #  If answer if False try to power up the board, else True
            if answer[1] is not True:
                print(f'POWER - {answer[1]} Powering On ...')

                #  Power ON module
                power_on()

            else:
                print(f"POWER - {answer[1]}")

            #  If board is powered and UART connection is True, check GSM signal strength.
            if self.ser.isOpen() and answer[1] is True:
                signal_strength = GSM(self.ser).read_signal_strength()
                sleep(1)
                get_serial_number = send_at('AT+GSN', serial_number, 1, self.ser)
                sleep(1)

                #  If serial number is correct, continue program, else stop it.
                if get_serial_number[1]:
                    sms_message = f'Jagoda powered ON\nGSM signal strength: {signal_strength}'

                    #  If sms_sender and send_sms are True send sms_message to phone_number
                    if self.send_sms and sms_sender:
                        GSM(self.ser).send_sms(phone_number, sms_message)
                        return True
                    return True


def power_on():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(4, GPIO.OUT)
    while True:
        GPIO.output(4, GPIO.LOW)
        sleep(4)
        GPIO.output(4, GPIO.HIGH)
        break
    GPIO.cleanup()
    sleep(10)

    return True

def power_down():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(4, GPIO.OUT)
    while True:
        GPIO.output(4, GPIO.LOW)
        sleep(4)
        GPIO.output(4, GPIO.HIGH)
        break
    GPIO.cleanup()
    sleep(10)

    return True
