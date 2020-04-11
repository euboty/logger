#!/usr/bin/env python

import sqlite3
import os
import glob

# global variables
db_name = '/home/pi/logger/templog.db'
savetill = '-3 month'

# use just once as global, used 2 times in script
conn = sqlite3.connect(db_name)

# stores temperature and date in database


def log_temperature(temp):

    curs = conn.cursor()
    curs.execute(
        "INSERT INTO temps values(datetime('now', 'localtime'), (?))", (temp,))
    conn.commit()



def delete_old():
    """deletes entrys older than savetill"""
    curs = conn.cursor()
    curs.execute(
        "DELETE FROM temps WHERE timestamp <= date('now', (?))", (savetill,))
    conn.commit()


def get_temp(devicefile):

    # with contextblock, closes file automatically
    with open(devicefile, 'r') as fileobj:
        lines = fileobj.readlines()

    # get the status from the end of line 1
    status = lines[0][-4:-1]

    # is the status is YES, get the temperature from line 2
    if status == "YES":
        tempstr = lines[1].split("t=")
        tempvalue = float(tempstr[1])/1000
        return tempvalue
    else:
        raise Exception(f"incorrect status: {status}")


def initialize():
    """use if sensor connected for the first time"""
    # enable kernel modules
    os.system('sudo modprobe w1-gpio')
    os.system('sudo modprobe w1-therm')

def read_temperature():
    # search for a device file that starts with 28
    devicelist = glob.glob('/sys/bus/w1/devices/28*')
    if not devicelist:
        raise Exception("could not find device")
    else:
        # append /w1slave to the device file
        w1devicefile = devicelist[0] + '/w1_slave'

    # get temperature from the device file
    try:
        temperature = get_temp(w1devicefile)
    except:
        # Sometimes reads fail on the first attempt
        # so we need to retry
        temperature = get_temp(w1devicefile)
    return temperature

def main():
    temperature = read_temperature()
    print("temperature = "+str(temperature))

    # store temperature in database
    log_temperature(temperature)

    # WENN SPEICHERPLATZ EIN PROBLEM SEIN SOLLTE AKTIVIEREN:
    # delete_old()
    conn.close()


# starting point
if __name__ == "__main__":
    main()
