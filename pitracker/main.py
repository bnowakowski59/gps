# !/usr/bin/env python3

from raspberry_hat.powerCFG import *
from raspberry_hat.gps_gnss_gprs_hat import *
from MPU.mpu import checkMPU
from mongoDB import mongoDB
from time import sleep

from format_date import formatDate

import serial

nr_seq = 1

if __name__ == "__main__":
    #  Opening serial port to gnss/gprs raspberry HAT.
    ser = SerialPort().open()

    #  Booting modem and check status.
    if PowerCFG(ser, True).boot_on():

        while True:
            #  Close PPPD internet connection.
            GPRS().closeConnection()

            #  Opening serial port to gnss/gprs raspberry HAT.
            ser = SerialPort().open()

            #  Creating empty moving speed list
            speed_list = []

            #  Check for gnss satellite fix,
            #  if fix will be found,
            #  get its positions, time and speed.
            #  Save speed measures to list.
            #  Repeat everything NUMBER_OF_COORD_READS times.
            for i in range(number_of_gnss_reads):
                latitude, longitude, date, speed = GPS(ser).get_gps_position()

                print(f'latitude: {latitude}\n'
                      f'longitude: {longitude}\n'
                      f'date: {date}\n'
                      f'speed: {speed:.2f}')

                if (latitude and longitude) > 0:
                    print(f'{nr_seq}')
                    date = formatDate(date)
                    gnss_coordinates = f'{nr_seq},{date},{latitude},{longitude}'
                    nr_seq += 1
                    with open(temporary_coordinates_file, 'a') as f:
                        f.write(gnss_coordinates)
                        f.write("\n")
                        f.close()

                    with open(test_coordinates_file, 'a') as f:
                        f.write(gnss_coordinates)
                        f.write("\n")
                        f.close()

                speed_list.append(speed)

                # If received an sms, report back to phone number.
                sms_to_send_flag = False
                sms = GSM(ser).read_sms()

                if 'Start' in sms:
                    sms_to_send_flag = True
                    if (latitude and longitude) > 0:
                        sms_message = f"http://maps.google.com/?q={latitude},{longitude}"
                    else:
                        sms_message = f"Brak pozycji GNSS.\nUrzadzenie nie wykrylo wiecej niz 4 satelity."

                if 'Sygnal' in sms:
                    sms_to_send_flag = True
                    csq = GSM(ser).read_signal_strength()
                    sms_message = f'GSM signal strength: {csq}'

                if sms_to_send_flag:
                    if sms_sender:
                        GSM(ser).send_sms(phone_number, sms_message)
                        sms_to_send_flag = False

                sleep(seconds_between_reads)

            #  Calculate average speed.
            average_speed = sum(speed_list) / number_of_gnss_reads
            print(f"average speed: {average_speed:.2f}")

            #  Sending positions from temporary csv file to database.
            if GPRS().openConnection():
                print(f"Checking connection to database ...")
                mongoDB(task_name, temporary_coordinates_file, device_id)
                print(f"Connection end.")
                GPRS().closeConnection()
                sleep(0.1)
                ser.close()

            #  If mpu_board is True, activate Multi Processing Unit.
            if not mpu_board:
                continue
            #  If avg. speed is high enought start MPU measurments.
            if average_speed > 3.0:
                print("Vehicle is moving. Continiue GNSS measurment ...")
                continue
            else:
                power_down()
                sms_message = checkMPU()

                if sms_message[1]:
                    ser = SerialPort().open()
                    PowerCFG(ser, False).boot_on()
                    
                    if sms_sender:
                        GSM(ser).send_sms(phone_number, sms_message[0])

                    continue
