#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Control class for TP-Link HS100 Smart Plug
"""

import datetime
import socket
import json
import sys
import json
import time


class HS100(object):
    '''
    Methods for controlling the HS100 smartplug
    '''

    encryption_key = 0xAB

    __udp_ip = ""
    __udp_port = 9999
    __alias = ""
    __device_id = ""
    __relay_state = 0

    # Public Methods

    def __init__(self, ip_address):
        '''
        Initialise the plug with an ip address
        '''

        # validate the ip address
        ip_array = ip_address.split(".")
        valid_ip = True
        try:
            if len(ip_array) == 4:
                for ipval in ip_array:
                    if int(ipval) < 0 or int(ipval) > 255:
                        valid_ip = False
            else:
                valid_ip = False
        except (RuntimeError, TypeError, ValueError):
            valid_ip = False

        if valid_ip:
            self.__udp_ip = ip_address

            # Parse the sysinfo JSON message to get the
            # status of the various parameters

            try:
                data = json.loads(self.status())

                json_formatted_str = json.dumps(data, indent=2)
                print(json_formatted_str)

                col1 = 'system'
                col2 = 'get_sysinfo'
                self.__alias = data[col1][col2]['alias']
                self.__relay_state = data[col1][col2]['relay_state']
                self.device_id = str(data[col1][col2]['deviceId'])

            except (RuntimeError, TypeError, ValueError) as exception:
                raise Exception(exception)
        else:
            raise ValueError('Invalid IPv4 IP address.')

    def status(self):
        '''
        Get the connection status from the bulb
        '''
        message = "{\"system\":{\"get_sysinfo\":{}}}"
        return self.__fetch_data(message)

    def on(self):
        """
        Set the plug to an on state
        """
        print("turn plug on")
        self.__relay_state = 1
        msg = '{"system":{"set_relay_state":{"state":1}}}'
        self.__update(msg)

    def off(self):
        """
        Set the plug to an off state
        """
        print("turn plug off")
        self.__relay_state = 1
        msg = '{"system":{"set_relay_state":{"state":0}}}'
        self.__update(msg)

    def reboot(self):
        '''
        Reboot the bulb
        '''
        self.__update("{\"smartlife.iot.common.system\":{\"reboot\":\
                      {\"delay\":1}}}")

    @property
    def alias(self):
        '''
        Get the device alias
        '''
        return self.__alias

    @alias.setter
    def alias(self, name):
        '''
        Set the device alias
        '''
        self.__update("{\"smartlife.iot.common.system\":{\"set_dev_alias\"\
                      :{\"alias\":\"" + name + "\"}}}")

    @property
    def time(self):
        '''
        Get the date and time from the device
        '''
        message = "{\"smartlife.iot.common.timesetting\":{\"get_time\":{}}}"
        device_time = datetime
        data = json.loads(self.__fetch_data(message))
        col1 = 'smartlife.iot.common.timesetting'
        device_time.year = data[col1]['get_time']['year']
        device_time.month = data[col1]['get_time']['month']
        device_time.day = data[col1]['get_time']['mday']
        device_time.hour = data[col1]['get_time']['hour']
        device_time.minute = data[col1]['get_time']['min']
        device_time.second = data[col1]['get_time']['sec']
        return device_time

    @time.setter
    def time(self, date):
        '''
        Set the date and time on the device
        '''
        if isinstance(date, datetime.datetime):
            self.__update("{\"smartlife.iot.common.timesetting\":{\"set_time\"\
                          :{\"year\":" + str(date.year) +
                          ",\"month\":" + str(date.month) +
                          ",\"mday\":" + str(date.day) +
                          ",\"hour\":" + str(date.hour) +
                          ",\"min\":" + str(date.minute) +
                          ",\"sec\":" + str(date.second) +
                          "}}}")
        else:
            raise ValueError('Invalid type: must pass a datetime object')
        return

    @property
    def timezone(self):
        '''
        Get the timezone from the device
        '''
        message = "{\"smartlife.iot.common.timesetting\":\
                   {\"get_timezone\":{}}}"

        data = json.loads(self.__fetch_data(message))
        col1 = 'smartlife.iot.common.timesetting'
        timezone = data[col1]['get_timezone']['index']
        return timezone

    @timezone.setter
    def timezone(self, timezone):
        '''
        Set the timezone on the device
        '''
        if timezone >= 0 and timezone <= 109:
            date = self.time
            self.__update("{\"smartlife.iot.common.timesetting\":\
                          {\"set_timezone\":{\"index\":" + str(timezone) +
                          ",\"year\":" + str(date.year) +
                          ",\"month\":" + str(date.month) +
                          ",\"mday\":" + str(date.day) +
                          ",\"hour\":" + str(date.hour) +
                          ",\"min\":" + str(date.minute) +
                          ",\"sec\":" + str(date.second) + "}}}")
        else:
            raise ValueError('Timezone out of range: 0 to 109')
        return

    @property
    def transition_period(self):
        '''
        Get the bulb transition period
        '''
        return self.__transition_period

    @transition_period.setter
    def transition_period(self, period):
        '''
        Set the plug transition period
        '''
        if period >= 0 and period <= 100000:
            self.__transition_period = period
        else:
            raise ValueError('transition_period out of range: 0 to 100000')

    # private methods

    @staticmethod
    def __encrypt(value, key):
        '''
        Encrypt the command string
        '''
        valuelist = list(value)

        for i in range(len(valuelist)):
            var = ord(valuelist[i])
            valuelist[i] = chr(var ^ int(key))
            key = ord(valuelist[i])
        if sys.version_info >= (3, 0):
            return bytearray("".join(valuelist).encode("latin_1"))  # python 3 fix
        else:
            return "".join(valuelist)

    @staticmethod
    def __decrypt(value, key):
        '''
        Decrypt the command string
        '''
        valuelist = list(value.decode("latin_1"))

        for i in range(len(valuelist)):
            var = ord(valuelist[i])
            valuelist[i] = chr(var ^ key)
            key = var

        return "".join(valuelist)

    def __update(self, message):
        '''
        Update the bulbs status
        '''
        enc_message = self.__encrypt(message, self.encryption_key)

        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.settimeout(5)
            sock.sendto(enc_message, (self.__udp_ip, self.__udp_port))
            data_received = False
            dec_data = ""
            while True:
                data, addr = sock.recvfrom(1024)  # buffer size is 1024 bytes
                dec_data = self.__decrypt(data, self.encryption_key)
                if "}}}" in dec_data:  # end of sysinfo message
                    data_received = True
                    break

            if data_received:
                if "\"err_code\":0" in dec_data:
                    return
                else:
                    raise RuntimeError("Plug returned error: " + dec_data)
            else:
                raise RuntimeError("Error connecting to Plug")
        except:
            raise RuntimeError("Error connecting to Plug")

    def __fetch_data(self, message):
        '''
        Fetch data from the device
        '''
        enc_message = self.__encrypt(message, self.encryption_key)

        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.settimeout(5)
            sock.sendto(enc_message, (self.__udp_ip, self.__udp_port))
            data_received = False
            dec_data = ""
            while True:
                data, addr = sock.recvfrom(1024)  # buffer size is 1024 bytes
                dec_data = self.__decrypt(data, self.encryption_key)
                if "}}}" in dec_data:  # end of sysinfo message
                    data_received = True
                    break

            if data_received:
                if "\"err_code\":0" in dec_data:
                    return dec_data
                else:
                    raise RuntimeError("Plug returned error: " + dec_data)
            else:
                raise RuntimeError("Error connecting to plug")
        except:
            raise RuntimeError("Error connecting to plug")


if __name__ == "__main__":
    plug = HS100('192.168.0.211')
    plug.on()
    time.sleep(1)
    plug.off()

    print(plug.status())
