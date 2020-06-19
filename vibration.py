#!/usr/bin/python3

import time

import board
import busio
import adafruit_adxl34x as adxl
from loguru import logger

from database import save_vibration

i2c = busio.I2C(board.SCL, board.SDA)
gyro = adxl.ADXL345(i2c)




def read_vibration():
    gyro.enable_motion_detection(threshold=20)
    # read the value once to clear any caches
    gyro.events['motion']
    time.sleep(1)
    motion_detected = gyro.events['motion']
    gyro.disable_motion_detection()
    return motion_detected


def main():
    result = read_vibration()
    logger.info(f"Motion: {result}")
    save_vibration(result)
    # if storage becomes a problem uncomment this
    # delete_old_vibrations()

if __name__ == "__main__":
    logger.add("/home/pi/logger/cron_log/vibration.log", rotation="2 MB", retention=5)

    try:
        main()
    except Exception:
        logger.exception("Top level error while reading vibrations")
