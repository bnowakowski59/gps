# !/usr/bin/env python3

from time import sleep


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
