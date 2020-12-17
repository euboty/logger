#!/usr/bin/env python

import glob

from loguru import logger

from database import save_temperature


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
    except Exception:
        # Sometimes reads fail on the first attempt
        # so we need to retry
        temperature = get_temp(w1devicefile)
    return temperature


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


def main():
    temperature = read_temperature()
    logger.trace(f"temperature = {temperature}")
    save_temperature(temperature)
    # if storage becomes a problem uncomment this
    # delete_old_temps()


if __name__ == "__main__":
    logger.add("/home/pi/logger/cron_log/temperature.log", rotation="2 MB", retention=5)

    try:
        main()
    except Exception:
        logger.exception("Top level error while reading the temperature")
