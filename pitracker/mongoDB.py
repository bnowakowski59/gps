# !/usr/bin/env python3

from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
import datetime
from interruptingcow import timeout


#  Connect and send data to mongoDB
def mongoDB(taskName, tempFile, device_id):
    CONNECTION_STRING = "mongodb://192.168.0.156:27017/meandb"

    try:
        connect = MongoClient(CONNECTION_STRING, serverSelectionTimeoutMS=60000)
        # print(f{connect.server_info()}')
        print(f"{connect.admin.command('ismaster')}")
        db = connect.meandb
        collection = db.gpsdatabase

        #  Read lines from __tmp_position.csv file.
        f = open(tempFile, 'r+')
        lines = f.read().splitlines()
        f.close()

        #  Split lines to time, latitude and longitude.
        try:
            with timeout(180, exception=RuntimeError):
                for i in lines:
                    array = i.split(",")
                    date_array = array[1].split("-")
                    time_iso = datetime.datetime(int(date_array[0]), int(date_array[1]),
                                                 int(date_array[2]), int(date_array[3]),
                                                 int(date_array[4]), int(date_array[5]), 0).replace(microsecond=0)
                    print(f"Sending {array[0]}, {time_iso}, {array[2]}, {array[3]}")

                    # post = [{"date": array[1],
                    #          "name": taskName,
                    #          "nr_seq": array[0],
                    #          "latitude": array[2],
                    #          "longitude": array[3],
                    #          "device_id": device_id
                    #          }]

                    post = [{"date": time_iso,
                             "name": taskName,
                             "nr_seq": array[0],
                             "latitude": array[2],
                             "longitude": array[3],
                             "device_id": device_id
                             }]

                    # collection.insert_one(post)
                    collection.insert_many(post)

                #  Delete all coordinates from temporary file.
                open(tempFile, 'w').close()

        except RuntimeError:
            print("didn't finish sending.")
        #  Delete all coordinates from temporary file.
        open(tempFile, 'w').close()

    except ConnectionFailure as err:
        print(err)

