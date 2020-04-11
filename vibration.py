#!/usr/bin/python3

from gpiozero import MotionSensor
from database import save_vibration

pir = MotionSensor(17, queue_len=1, sample_rate=100)


def main():
    result = read_vibration()
    print(f"Motion: {result}")
    save_vibration(result)

def read_vibration():
    pir.wait_for_motion(timeout=5)
    return pir.motion_detected

if __name__ == "__main__":
    main()
