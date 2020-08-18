#!/usr/bin/python

# Libraries
import RPi.GPIO as GPIO
from tplight import LB130
from tpplug import HS100
from distance import DistanceSensor
import time

if __name__ == '__main__':
    plug = HS100('192.168.0.211')
    plug.off()
    sensor = DistanceSensor()
    dist_threshold_upper = 160
    dist_threshold_lower = 140

    try:
        while True:
            dist = sensor.get_distance()
            print("Measured Distance = %.1f cm" % dist)

            if dist < dist_threshold_lower or dist > dist_threshold_upper:
                print("door opens: light on for 10 seconds!")
                plug.on()
                time.sleep(10)
                plug.off()

            time.sleep(1)

            # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()
