import os, sys

#  Set phone number where sms will be send.
phone_number = '572720038'

#  Serial number of HAT
serial_number = '867717033828212'

# Device id for DB.
device_id = '123456'

#  Set number of GNSS reads, time between them, and mpu sleep time.
number_of_gnss_reads = 10
seconds_between_reads = 30
timeout_mpu = 10

#  Number of tries to get fix, after False go to mpu6050 module
fix_iterations = 10

#  Set path to files.
temporary_coordinates_file = '/home/pi/pitracker/logs/__tmp_position.csv'
test_coordinates_file = '/home/pi/pitracker/logs/__test_position.csv'

#  Set task name.
task_name = 'Test_Wawelska'

#  Set port output.
PORT = '/dev/serial0'

#  If mpu6050 board will be used set to True else False.
mpu_board = True

#  While True - allow send sms.
sms_sender = True

#  if True Print function will work.
print_status = True

if not print_status:
    sys.stdout = open(os.devnull, 'w')


