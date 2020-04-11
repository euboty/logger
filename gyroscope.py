#!/usr/bin/python3

import time

import board
import busio
import adafruit_adxl34x as adxl

i2c = busio.I2C(board.SCL, board.SDA)
gyro = adxl.ADXL345(i2c)


def main():
    x, y, z = gyro.acceleration
    print(f"x={x} - y={y} - z={z}")

    print(f"Motion: {gyro.events['motion']}")


if __name__ == "__main__":
    gyro.enable_motion_detection(threshold=50)
    time.sleep(1)
    main()
    gyro.disable_motion_detection()
