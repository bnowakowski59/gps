# !/usr/bin/env python3
import subprocess

from raspberry_hat.sendAT import send_at
from time import sleep
from raspberry_hat.config import *


class GPRS:
    """
    GPRS module from HAT

    """

    def openConnection(self):
        """
        Connect to pppd network from /etc/ppp/pears/gprs
        """

        print(f"Opening PPPD connection ...")
        #  Check if PPPD is running by looking into syslog output.
        output1 = subprocess.check_output("cat /var/log/syslog | grep pppd | tail -1", shell=True)
        if b"secondary DNS address" not in output1 and b"locked" not in output1:
            while True:
                #  Start GPRS process.
                subprocess.Popen("sudo pon gprs", shell=True)
                sleep(2)
                output2 = subprocess.check_output("cat /var/log/syslog | grep pppd | tail -1", shell=True)
                # print(f"Output2: {output2}")
                if b"script failed" not in output2:
                    print(f"PPPD connection opened - {True}")
                    return True
                    sleep(0.5)
                else:
                    print(f"Connect error")
                    sleep(0.5)

    def closeConnection(self):
        """
        Disconect from pppd network from /etc/ppp/pears/gprs
        """
        print(f"Closing PPPD connection ...")
        #  Stop GPRS process.
        subprocess.Popen('sudo poff gprs', shell=True)
        #  Chceck if connection is terminated.
        while True:
            output = subprocess.check_output("cat /var/log/syslog | grep pppd | tail -1", shell=True)

            if b'Exit' or b'None' in output:
                print(f"PPPD connection closed - {True}")
                sleep(0.5)
                return True


class GPS:
    """
    GPS module from HAT

    """

    def __init__(self, ser):
        self.ser = ser

    def get_gps_position(self):
        global fix_iterations
        answer = 0
        i = 0
        rec_buff = ''

        send_at('AT+CGNSPWR=1', 'OK', 1, self.ser)
        sleep(1)

        while True:
            answer = send_at('AT+CGNSINF', '+CGNSINF: 1,1,', 1, self.ser)
            print(answer)

            if '+CGNSINF: 1,1,' in answer[0]:
                array = answer[0].split(",")
                timeSplit = array[2].split(".")
                dateString = timeSplit[0]  # time
                latitudeFloat = float(array[3])  # latitude
                longitudeFloat = float(array[4])  # longitude
                speedString = float(array[6])  # speed

                return latitudeFloat, longitudeFloat, dateString, speedString

            if '+CGNSINF: 1,0,' in answer[0]:
                print("Fix not found ...")
                i += 1

                if i == fix_iterations:
                    latitudeFloat = 0
                    longitudeFloat = 0
                    dateString = '0'
                    speedString = 0
                    return latitudeFloat, longitudeFloat, dateString, speedString

                sleep(1)
                continue

            if '+CGNSINF: 0,,,,' or '+CGNSINF: 0,0,' in answer[0]:
                send_at('AT+CGNSPWR=1', 'OK', 1, self.ser)
                sleep(1)
                continue


class GSM:
    """
    GSM module from HAT.
    """

    def __init__(self, ser):
        self.ser = ser

    def send_sms(self, phone_number, message):
        """
        Send SMS to phone_number
        """

        phone_number = f'"{phone_number}"'
        send_at('AT+CMGF=1', 'OK', 1, self.ser)
        send_at('AT+CMGS=' + phone_number, '', 1, self.ser)
        self.ser.write(message.encode() + b"\r")
        self.ser.write(bytes([26]))

        print(f"SMS send to {phone_number}")

    def read_sms(self):
        """
        Read income SMS, return message state on output:
        Start
        """

        send_at('AT+CMGF=1', 'OK', 1, self.ser)
        answer = send_at('AT+CMGL="REC UNREAD"', phone_number, 1, self.ser)
        print(answer)
        sleep(1)
        self.ser.write(b'AT+CMGD=1,4\r')
        if phone_number in answer[0]:
            if 'Start\r\n' in answer[0]:
                return 'Start'

            if 'Sygnal\r\n' in answer[0]:
                return 'Sygnal'

            else:
                return 'None'

        return 'None'

    def read_signal_strength(self):
        """
        Return an integer between 1 and 99, representing the current
        signal strength of the GSM network, False if we don't know, or
        None if the modem can't report it.
        """

        while True:
            answer = send_at('AT+CSQ', 'CSQ', 1, self.ser)

            if "+CSQ: " in answer[0]:
                try:
                    answer_array = answer[0].split(",")
                    csq = int(answer_array[0].split()[2])
                    return csq if csq < 99 else False

                except IndexError as err:
                    print(err)


def send_at(command, answer, timeout, ser):
    rec_buff = ''
    ser.write((command + '\r\n').encode())
    sleep(timeout)
    if ser.inWaiting():
        sleep(0.01)
        rec_buff = ser.read(ser.inWaiting())
    if rec_buff != '':
        if answer not in rec_buff.decode():
            # print(command + ' ERROR')
            # print(command + ' back:\t' + rec_buff.decode())
            return rec_buff.decode(), False
        else:
            return rec_buff.decode(), True
    else:
        return rec_buff, False
