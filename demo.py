#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Demo for the TP-Link A19-LB130 RBGW WiFi bulb
'''


import time
from tplight import LB130

def main():
    '''
    Main program function
    '''

    # create an instance of the light with its IP address
    light = LB130("192.168.0.142")

    # fetch the details for the light
    print("Device ID: " + light.device_id)
    print("Alias: " + light.alias)
    print("Wattage: " + str(light.wattage))

    light.off()
    time.sleep(1)

    light.on()
    time.sleep(1)

    # brightness(light)
    # flashing_light(light)


def flashing_light(light):
    print("Flashing the light")
    light.off()
    time.sleep(2)

    light.on()
    time.sleep(2)

    light.off()
    time.sleep(2)

    light.on()
    time.sleep(2)

    light.off()
    time.sleep(2)

    light.on()
    time.sleep(2)

    print("Done flashing")

def brightness(light):
    print("set brightness")
    # set the brightness
    light.brightness = 1
    time.sleep(2)

    light.brightness = 20
    time.sleep(2)

    light.brightness = 40
    time.sleep(2)

    light.brightness = 60
    time.sleep(2)

    light.brightness = 80
    time.sleep(2)

    light.brightness = 100
    time.sleep(2)

    print("brightness done")

def saturation(light):
    print("set saturation")
    # set the saturation
    light.saturation = 10
    time.sleep(2)

    # set the saturation
    light.saturation = 30
    time.sleep(2)

    # set the saturation
    light.saturation = 50
    time.sleep(2)

    # set the saturation
    light.saturation = 70
    time.sleep(2)

    # set the saturation
    light.saturation = 100
    time.sleep(2)

    print("saturation done")

def temperature(light):
    print("set temp")
    light.temperature = 2500
    time.sleep(2)

    light.temperature = 9000
    time.sleep(2)

    light.temperature = 3800
    time.sleep(2)

    light.temperature = 5000
    time.sleep(2)

    print("temp done")

if __name__ == "__main__":
    main()

