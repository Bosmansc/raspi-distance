#!/usr/bin/python

# Libraries
import RPi.GPIO as GPIO
import time


class DistanceSensor(object):
    """
    Methods for controlling the raspi distance sensor
    """

    # set GPIO Pins
    __GPIO_TRIGGER = 7
    __GPIO_ECHO = 11

    def __init__(self):
        """
        Initialise the distance sensor
        """

        # GPIO Mode (BOARD / BCM)
        GPIO.setmode(GPIO.BOARD)

        # set GPIO direction (IN / OUT)
        GPIO.setup(self.__GPIO_TRIGGER, GPIO.OUT)
        GPIO.setup(self.__GPIO_ECHO, GPIO.IN)

    def get_distance(self):
        # set Trigger to HIGH
        GPIO.output(self.__GPIO_TRIGGER, True)

        # set Trigger after 0.01ms to LOW
        time.sleep(0.00001)
        GPIO.output(self.__GPIO_TRIGGER, False)

        start_time = time.time()
        stop_time = time.time()

        # save StartTime
        while GPIO.input(self.__GPIO_ECHO) == 0:
            start_time = time.time()

        # save time of arrival
        while GPIO.input(self.__GPIO_ECHO) == 1:
            stop_time = time.time()

        # time difference between start and arrival
        time_elpased = stop_time - start_time
        # multiply with the sonic speed (34300 cm/s)
        # and divide by 2, because there and back
        distance = (time_elpased * 34300) / 2

        return distance


if __name__ == '__main__':
    sensor = DistanceSensor()
    print(sensor.get_distance())
