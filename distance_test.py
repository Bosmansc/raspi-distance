#!/usr/bin/python

#Libraries
import RPi.GPIO as GPIO
import time
from tplight import LB130

#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BOARD)

#set GPIO Pins
GPIO_TRIGGER = 7
GPIO_ECHO = 11

#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

def distance():
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)

    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)

    StartTime = time.time()
    StopTime = time.time()

    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()

    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()

    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2

    return distance

 
if __name__ == '__main__':

    print("Initialize smart bulb")
    # create an instance of the light with its IP address
    light = LB130("192.168.0.142")

    light.off()
    time.sleep(1)
    light.on()

    try:
        while True:
            print("Measuring distance...")
            dist = distance()
            print("Measured Distance = %.1f cm" % dist)

            dist_threshold = 5

            if dist < dist_threshold:
                print("too close: light off")
                light.off()

            if dist > dist_threshold:
                print("far enough: light on")
                light.on()

            time.sleep(1)
 
        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()